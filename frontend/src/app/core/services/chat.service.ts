import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}
  sendMessage(message: string) {
    return this.http.post(`${this.apiUrl}/chat`, {
      message: message,
      user_id: "student_1"   // 🔥 simulate user
    });
  }
}