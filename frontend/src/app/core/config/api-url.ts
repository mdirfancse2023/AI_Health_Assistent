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

function getBaseHref(): string {
  if (typeof document === 'undefined') {
    return '';
  }

  const href = document.querySelector('base')?.getAttribute('href') ?? '/';
  if (href === '/') {
    return '';
  }

  return href.endsWith('/') ? href.slice(0, -1) : href;
}

export function getApiUrl(): string {
  if (typeof window === 'undefined') {
    return '/api';
  }

  const configured = window.__APP_CONFIG__?.apiUrl;
  if (configured) {
    return normalizeApiUrl(configured);
  }

  return `${getBaseHref()}/api`;
}

