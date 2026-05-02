const TRACKING_PARAMS = new Set([
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'fbclid', 'gclid',
]);

export function canonicalizeUrl(input?: string | null): string | undefined {
  const value = String(input || '').trim();
  if (!value) return undefined;
  const withScheme = /^[a-z][a-z0-9+.-]*:/i.test(value) ? value : `https://${value}`;
  let url: URL;
  try {
    url = new URL(withScheme);
  } catch {
    return undefined;
  }
  if (url.protocol === 'http:') url.protocol = 'https:';
  url.hostname = url.hostname.toLowerCase().replace(/^www\./, '');
  for (const param of Array.from(url.searchParams.keys())) {
    if (TRACKING_PARAMS.has(param.toLowerCase())) url.searchParams.delete(param);
  }
  if (url.pathname.length > 1 && url.pathname.endsWith('/')) url.pathname = url.pathname.slice(0, -1);
  url.hash = '';
  return url.toString();
}

export function normalizeDoi(input?: string | null): string | undefined {
  const value = String(input || '')
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\/(dx\.)?doi\.org\//, '')
    .replace(/^doi:/, '')
    .trim();
  return /^10\.\S+\/\S+$/.test(value) ? value : undefined;
}

function isbn10CheckDigit(body: string) {
  let sum = 0;
  for (let i = 0; i < 9; i += 1) sum += (10 - i) * Number(body[i]);
  const remainder = 11 - (sum % 11);
  if (remainder === 10) return 'X';
  if (remainder === 11) return '0';
  return String(remainder);
}

function isbn13CheckDigit(body: string) {
  let sum = 0;
  for (let i = 0; i < 12; i += 1) sum += Number(body[i]) * (i % 2 === 0 ? 1 : 3);
  return String((10 - (sum % 10)) % 10);
}

export function normalizeIsbn(input?: string | null): string | undefined {
  const value = String(input || '').replace(/[\s-]/g, '').toUpperCase();
  if (/^\d{9}[0-9X]$/.test(value)) return isbn10CheckDigit(value.slice(0, 9)) === value[9] ? value : undefined;
  if (/^\d{13}$/.test(value)) return isbn13CheckDigit(value.slice(0, 12)) === value[12] ? value : undefined;
  return undefined;
}

export function normalizeTextKey(input?: string | null): string {
  return String(input || '')
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .replace(/\s+/g, ' ');
}
