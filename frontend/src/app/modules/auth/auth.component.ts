import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  mode: 'login' | 'signup' = 'login';
  identifier = '';
  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  isSubmitting = false;
  errorMessage = '';

  setMode(mode: 'login' | 'signup'): void {
    this.mode = mode;
    this.errorMessage = '';
  }

  submit(): void {
    this.errorMessage = '';

    if (this.mode === 'signup') {
      if (!this.username.trim() || !this.email.trim() || !this.password.trim()) {
        this.errorMessage = 'All signup fields are required.';
        return;
      }

      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Passwords do not match.';
        return;
      }
    } else if (!this.identifier.trim() || !this.password.trim()) {
      this.errorMessage = 'Username/email and password are required.';
      return;
    }

    this.isSubmitting = true;

    const request$ = this.mode === 'signup'
      ? this.authService.signup(this.username.trim(), this.email.trim(), this.password)
      : this.authService.login(this.identifier.trim(), this.password);

    request$.subscribe({
      next: () => {
        this.isSubmitting = false;
        this.router.navigateByUrl(this.route.snapshot.queryParamMap.get('redirectTo') || '/chat');
      },
      error: (error: HttpErrorResponse) => {
        this.isSubmitting = false;
        this.errorMessage = error.error?.detail || 'Authentication failed. Please try again.';
      }
    });
  }
}
