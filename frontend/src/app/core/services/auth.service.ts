import { computed, inject, Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { getApiUrl } from '../config/api-url';

export interface AuthUser {
  id: number;
  username: string;
  email: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}

const TOKEN_STORAGE_KEY = 'auth_token';
const USER_STORAGE_KEY = 'auth_user';

function isBrowser(): boolean {
  return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
}

function decodeTokenPayload(token: string): { exp?: number } | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      return null;
    }

    const payload = parts[1];
    const normalized = payload.replace(/-/g, '+').replace(/_/g, '/');
    const padding = '='.repeat((4 - (normalized.length % 4)) % 4);
    const decoded = atob(`${normalized}${padding}`);
    return JSON.parse(decoded);
  } catch {
    return null;
  }
}

function clearStoredSession(): void {
  if (!isBrowser()) {
    return;
  }

  localStorage.removeItem(TOKEN_STORAGE_KEY);
  localStorage.removeItem(USER_STORAGE_KEY);
}

export function getStoredAccessToken(): string | null {
  if (!isBrowser()) {
    return null;
  }

  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (!token) {
    return null;
  }

  const payload = decodeTokenPayload(token);
  if (payload?.exp && payload.exp * 1000 <= Date.now()) {
    clearStoredSession();
    return null;
  }

  return token;
}

function getStoredUser(): AuthUser | null {
  if (!isBrowser()) {
    return null;
  }

  const rawUser = localStorage.getItem(USER_STORAGE_KEY);
  if (!rawUser) {
    return null;
  }

  try {
    return JSON.parse(rawUser) as AuthUser;
  } catch {
    clearStoredSession();
    return null;
  }
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly apiUrl = getApiUrl();

  readonly currentUser = signal<AuthUser | null>(getStoredAccessToken() ? getStoredUser() : null);
  readonly isAuthenticated = computed(() => this.currentUser() !== null && getStoredAccessToken() !== null);

  signup(username: string, email: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/signup`, {
      username,
      email,
      password
    }).pipe(tap((response) => this.persistSession(response)));
  }

  login(identifier: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/login`, {
      identifier,
      password
    }).pipe(tap((response) => this.persistSession(response)));
  }

  logout(): void {
    clearStoredSession();
    this.currentUser.set(null);
    this.router.navigateByUrl('/auth');
  }

  getToken(): string | null {
    return getStoredAccessToken();
  }

  private persistSession(response: AuthResponse): void {
    if (!isBrowser()) {
      return;
    }

    localStorage.setItem(TOKEN_STORAGE_KEY, response.access_token);
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(response.user));
    this.currentUser.set(response.user);
  }
}
