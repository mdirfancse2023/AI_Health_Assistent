import { Component, signal, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements AfterViewInit {

  emotionData = signal<Record<string, number>>({});
  trendData = signal<Record<string, number>>({});

  constructor(private http: HttpClient) {}

  ngAfterViewInit() {
    this.loadData();
  }

  loadData() {
    this.http.get<any>('http://127.0.0.1:8000/analytics/emotions')
      .subscribe(data => {
        console.log("EMOTION DATA:", data);
        this.emotionData.set(data);
        this.createEmotionChart(data);
      });

    this.http.get<any>('http://127.0.0.1:8000/analytics/trend')
      .subscribe(data => {
        console.log("TREND DATA:", data);
        this.trendData.set(data);
        this.createTrendChart(data);
      });
  }

  createEmotionChart(data: any) {
    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart('emotionChart', {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
            data: values,
            backgroundColor: [
                '#4CAF50',   // green
                '#FF5252',   // red
                '#FFC107',   // yellow
                '#2196F3'    // blue
            ]
        }]
      }
    });
  }

  createTrendChart(data: any) {
    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart('trendChart', {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
            label: 'Chats per Day',
            data: values,
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.2)',
            fill: true,
            tension: 0.4
         }]
      }
    });
  }
}