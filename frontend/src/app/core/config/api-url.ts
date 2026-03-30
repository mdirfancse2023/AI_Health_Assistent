declare global {
  interface Window {
    __APP_CONFIG__?: {
      apiUrl?: string;
    };
  }
}

function normalizeApiUrl(value: string | undefined): string {
  if (!value) {
    return '/api';
  }

  return value.endsWith('/') ? value.slice(0, -1) : value;
}

export function getApiUrl(): string {
  if (typeof window === 'undefined') {
    return '/api';
  }

  return normalizeApiUrl(window.__APP_CONFIG__?.apiUrl);
}

