import { Component, OnInit, Inject, inject } from '@angular/core';
import { Router, RouterModule, RouterOutlet } from '@angular/router';
import { CommonModule, DOCUMENT } from '@angular/common';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent implements OnInit {
  isDarkMode = false;
  protected readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  constructor(@Inject(DOCUMENT) private document: Document) {}

  ngOnInit() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      this.isDarkMode = true;
      this.document.documentElement.setAttribute('data-theme', 'dark');
    }
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    if (this.isDarkMode) {
      this.document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    } else {
      this.document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
    }
  }

  logout() {
    this.authService.logout();
  }

  isAuthMode(mode: 'login' | 'signup'): boolean {
    if (!this.router.url.startsWith('/auth')) {
      return false;
    }

    const modeParam = this.router.parseUrl(this.router.url).queryParams['mode'];
    return (modeParam ?? 'login') === mode;
  }
}
