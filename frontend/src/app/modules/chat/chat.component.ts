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
  messages = signal<any[]>([]);   // 🔥 SIGNAL

  constructor(private chatService: ChatService) {}

  trackByFn(index: number, item: any) {
    return index;
  }

  sendMessage() {
    if (!this.inputMessage.trim()) return;

    const userMessage = this.inputMessage;

    // ✅ Add user message
    this.messages.set([
      ...this.messages(),
      { sender: 'user', text: userMessage }
    ]);

    this.inputMessage = '';

    // ✅ Add typing
    this.messages.set([
      ...this.messages(),
      { sender: 'bot', text: 'Typing...' }
    ]);

    const typingIndex = this.messages().length - 1;

    this.chatService.sendMessage(userMessage).subscribe({
      next: (res: any) => {
        const updated = [...this.messages()];

        updated[typingIndex] = {
          sender: 'bot',
          text: res.response
        };

        this.messages.set(updated);   // 🔥 triggers UI instantly
      },
      error: () => {
        const updated = [...this.messages()];

        updated[typingIndex] = {
          sender: 'bot',
          text: 'Error connecting to server'
        };

        this.messages.set(updated);
      }
    });
  }
}