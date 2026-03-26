import { Component, NgZone } from '@angular/core';
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

  inputMessage: string = '';
  messages: any[] = [];

  constructor(
    private chatService: ChatService,
    private ngZone: NgZone
  ) {}

  trackByFn(index: number, item: any) {
    return index;
  }

  sendMessage() {
  if (!this.inputMessage.trim()) return;

  const userMessage = this.inputMessage;

  // Add user message
  this.messages.push({
    sender: 'user',
    text: userMessage
  });

  this.inputMessage = '';

  // Add typing
  this.messages.push({
    sender: 'bot',
    text: 'Typing...'
  });

  const typingIndex = this.messages.length - 1;

  this.chatService.sendMessage(userMessage).subscribe({
    next: (res: any) => {
      console.log("API RESPONSE:", res);

      // 🔥 FINAL FIX
      setTimeout(() => {
        this.messages[typingIndex] = {
          sender: 'bot',
          text: res.response
        };

        // force new reference
        this.messages = [...this.messages];
      }, 0);
    },
    error: () => {
      setTimeout(() => {
        this.messages[typingIndex] = {
          sender: 'bot',
          text: 'Error connecting to server'
        };

        this.messages = [...this.messages];
      }, 0);
    }
  });
}
}