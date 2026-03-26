import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/chat`, {
      message: message,
      user_id: "student_1"   // 🔥 simulate user
    });
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