import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../core/services/chat.service';

declare var marked: any;

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {

  inputMessage = '';
  messages = signal<any[]>([]);
  
  // Daily Check-in state
  showCheckinModal = false;
  stressLevel: number = 5;
  academicFocus: number = 5;

  constructor(private chatService: ChatService) {}

  async sendMessage() {
    if (!this.inputMessage.trim()) return;

    const userMessage = this.inputMessage;
    
    this.messages.set([
      ...this.messages(),
      { sender: 'user', text: userMessage }
    ]);
    this.inputMessage = '';

    // Typing indicator logic
    this.messages.set([
      ...this.messages(),
      { sender: 'bot', text: '<i>Thinking...</i>', rawText: '', id: null, rated: false }
    ]);

    const typingIndex = this.messages().length - 1;

    try {
      const stream = this.chatService.sendMessageStream(userMessage);
      
      let isFirstChunk = true;

      for await (const data of stream) {
        const updated = [...this.messages()];
        const botMsg = updated[typingIndex];

        if (isFirstChunk && data.chunk !== undefined) {
           botMsg.text = ''; // Clear indicator
           isFirstChunk = false;
        }

        if (data.chunk !== undefined) {
           botMsg.rawText += data.chunk;
           // Dynamically compile Raw Markdown -> Safe HTML iteratively
           botMsg.text = marked.parse(botMsg.rawText);
        } else if (data.chat_id !== undefined) {
           // Database Hook successfully completed in background
           botMsg.id = data.chat_id;
        }
        
        this.messages.set(updated);
      }
    } catch (e) {
        console.error("Stream failed:", e);
        const updated = [...this.messages()];
        updated[typingIndex].text = '<span style="color: red">Error connecting to server stream.</span>';
        this.messages.set(updated);
    }
  }

  rateResponse(msg: any, score: number) {
    if (!msg.id || msg.rated) return;
    this.chatService.sendFeedback(msg.id, score).subscribe();
    msg.rated = true;
  }

  submitCheckin() {
    this.chatService.sendCheckin(this.stressLevel, this.academicFocus).subscribe();
    this.showCheckinModal = false;
  }
}