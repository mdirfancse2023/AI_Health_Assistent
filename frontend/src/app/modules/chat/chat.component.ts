import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../core/services/chat.service';

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

  sendMessage() {
    if (!this.inputMessage.trim()) return;

    const userMessage = this.inputMessage;
    
    this.messages.set([
      ...this.messages(),
      { sender: 'user', text: userMessage }
    ]);
    this.inputMessage = '';

    // Typiny indicator
    this.messages.set([
      ...this.messages(),
      { sender: 'bot', text: 'Typing...', id: null, rated: false }
    ]);

    const typingIndex = this.messages().length - 1;

    this.chatService.sendMessage(userMessage).subscribe({
      next: (res: any) => {
        const updated = [...this.messages()];
        updated[typingIndex] = {
          sender: 'bot',
          text: res.response,
          id: res.chat_id,         // Store chat_id for feedback
          rated: false
        };
        this.messages.set(updated);
      },
      error: () => {
        const updated = [...this.messages()];
        updated[typingIndex] = {
          sender: 'bot',
          text: 'Error connecting to server',
          id: null,
          rated: false
        };
        this.messages.set(updated);
      }
    });
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