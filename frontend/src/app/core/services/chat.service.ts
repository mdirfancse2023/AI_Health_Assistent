import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = process.env['NG_APP_API_URL'] || '/api';

  constructor(private http: HttpClient) {}

  async *sendMessageStream(message: string): AsyncGenerator<any, void, unknown> {
    const response = await fetch(`${this.apiUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message, user_id: 'student_1' })
    });

    if (!response.body) throw new Error('ReadableStream not supported');

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // keep partial chunk

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.slice(6).trim();
          if (dataStr === '[DONE]') return;
          if (dataStr) {
            try {
              yield JSON.parse(dataStr);
            } catch (e) {
              console.error("Partial JSON chunk warning", e);
            }
          }
        }
      }
    }
  }

  sendFeedback(chatId: number, score: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/chat/feedback/${chatId}`, {
      score: score
    });
  }

  sendCheckin(stressLevel: number, academicFocus: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/chat/checkin`, {
      user_id: "student_1",
      stress_level: stressLevel,
      academic_focus: academicFocus
    });
  }
}
