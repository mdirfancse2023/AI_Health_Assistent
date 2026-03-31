import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { TimeoutError, timeout } from 'rxjs';
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
  private readonly destroyRef = inject(DestroyRef);

  mode: 'login' | 'signup' = 'login';
  identifier = '';
  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  isSubmitting = false;
  errorMessage = '';
  attemptedSubmit = false;

  constructor() {
    this.route.queryParamMap
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((params) => {
        this.setMode(params.get('mode') === 'signup' ? 'signup' : 'login');
      });
  }

  setMode(mode: 'login' | 'signup'): void {
    this.mode = mode;
    this.errorMessage = '';
    this.attemptedSubmit = false;

    if (mode === 'login' && !this.identifier.trim()) {
      this.identifier = this.username.trim() || this.email.trim();
    }
  }

  submit(): void {
    this.errorMessage = '';
    this.attemptedSubmit = true;

    if (this.mode === 'signup') {
      if (this.signupValidationMessage) {
        this.errorMessage = this.signupValidationMessage;
        return;
      }
    } else if (this.loginValidationMessage) {
      this.errorMessage = this.loginValidationMessage;
      return;
    }

    this.isSubmitting = true;

    const request$ = this.mode === 'signup'
      ? this.authService.signup(this.username.trim(), this.email.trim(), this.password)
      : this.authService.login(this.identifier.trim(), this.password);

    request$
      .pipe(timeout(7000))
      .subscribe({
      next: () => {
        this.isSubmitting = false;
        this.router.navigateByUrl(this.route.snapshot.queryParamMap.get('redirectTo') || '/chat');
      },
      error: (error: unknown) => {
        this.isSubmitting = false;
        this.errorMessage = this.getErrorMessage(error);
      }
    });
  }

  private getErrorMessage(error: unknown): string {
    if (error instanceof TimeoutError) {
      return 'Login request took too long. Please try again.';
    }

    if (!(error instanceof HttpErrorResponse)) {
      return 'Authentication failed. Please check your details and try again.';
    }

    const detail = error.error?.detail;

    if (typeof detail === 'string' && detail.trim()) {
      return detail;
    }

    if (Array.isArray(detail) && detail.length > 0) {
      const firstError = detail[0];
      if (typeof firstError?.msg === 'string' && firstError.msg.trim()) {
        return firstError.msg;
      }
    }

    if (error.status === 0) {
      return 'Unable to reach the server. Please try again in a moment.';
    }

    return 'Authentication failed. Please check your details and try again.';
  }

  get usernameValidationMessage(): string {
    if (!this.username.trim()) {
      return 'Username is required.';
    }

    if (this.username.trim().length < 3) {
      return 'Username must be at least 3 characters.';
    }

    return '';
  }

  get emailValidationMessage(): string {
    const email = this.email.trim();

    if (!email) {
      return 'Email is required.';
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return 'Enter a valid email address.';
    }

    return '';
  }

  get passwordValidationMessage(): string {
    if (!this.password) {
      return 'Password is required.';
    }

    if (this.password.length < 8) {
      return 'Password must be at least 8 characters.';
    }

    return '';
  }

  get confirmPasswordValidationMessage(): string {
    if (!this.confirmPassword) {
      return 'Please confirm your password.';
    }

    if (this.password !== this.confirmPassword) {
      return 'Passwords do not match.';
    }

    return '';
  }

  get identifierValidationMessage(): string {
    if (!this.identifier.trim()) {
      return 'Username or email is required.';
    }

    return '';
  }

  get signupValidationMessage(): string {
    return (
      this.usernameValidationMessage ||
      this.emailValidationMessage ||
      this.passwordValidationMessage ||
      this.confirmPasswordValidationMessage
    );
  }

  get loginValidationMessage(): string {
    return this.identifierValidationMessage || this.passwordValidationMessage;
  }

  showFieldError(message: string, shouldShow: boolean): boolean {
    return shouldShow && !!message;
  }
}
