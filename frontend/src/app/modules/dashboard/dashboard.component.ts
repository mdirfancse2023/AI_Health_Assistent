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
  effectivenessScore = signal<number>(0);
  stressAcademicData = signal<any[]>([]);

  constructor(private http: HttpClient) {}

  ngAfterViewInit() {
    this.loadData();
  }

  loadData() {
    this.http.get<any>('http://127.0.0.1:8000/analytics/emotions')
      .subscribe(data => {
        this.emotionData.set(data);
        this.createEmotionChart(data);
      });

    this.http.get<any>('http://127.0.0.1:8000/analytics/trend')
      .subscribe(data => {
        this.trendData.set(data);
        this.createTrendChart(data);
      });

    this.http.get<any>('http://127.0.0.1:8000/analytics/effectiveness')
      .subscribe(data => {
        this.effectivenessScore.set(data.score);
      });

    this.http.get<any[]>('http://127.0.0.1:8000/analytics/stress_academic')
      .subscribe(data => {
        this.stressAcademicData.set(data);
        if(data && data.length > 0) {
           this.createStressChart(data);
        }
      });
  }

  createEmotionChart(data: any) {
    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart('emotionChart', {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
            data: values,
            backgroundColor: [
                '#10b981',   // happy
                '#ef4444',   // stress
                '#3b82f6',   // sad
                '#f59e0b',   // anxiety
                '#6b7280'    // neutral
            ],
            borderWidth: 0
        }]
      },
      options: {
        cutout: '70%',
        plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 13 } } } }
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
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99, 102, 241, 0.2)',
            fill: true,
            tension: 0.4
         }]
      },
      options: {
         plugins: { legend: { display: false } },
         scales: { 
             x: { 
                 ticks: { color: '#94a3b8' },
                 grid: { color: 'rgba(148, 163, 184, 0.1)' }
             },
             y: { 
                 ticks: { color: '#94a3b8' },
                 grid: { color: 'rgba(148, 163, 184, 0.1)' }
             }
         }
      }
    });
  }

  createStressChart(data: any[]) {
    const labels = data.map(d => d.date);
    const stress = data.map(d => d.stress_level);
    const focus = data.map(d => d.academic_focus);

    new Chart('stressChart', {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Stress Level',
            data: stress,
            backgroundColor: '#ef4444',
            borderRadius: 6
          },
          {
            label: 'Academic Focus',
            data: focus,
            backgroundColor: '#3b82f6',
            borderRadius: 6
          }
        ]
      },
      options: {
        plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 13 } } } },
        scales: { 
            x: { 
                ticks: { color: '#94a3b8' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' }
            },
            y: { 
                ticks: { color: '#94a3b8' },
                grid: { color: 'rgba(148, 163, 184, 0.1)' }
            }
        }
      }
    });
  }
}