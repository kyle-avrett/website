import { SITE } from '../config';

export function formatDate(
    date: Date | string,
    options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' },
): string {
    const value = typeof date === 'string' ? new Date(date) : date;
    if (Number.isNaN(value.getTime())) return '';
    if (SITE.isoDates) return value.toISOString().slice(0, 10);
    return new Intl.DateTimeFormat('en-US', options).format(value);
}

export function isoDate(date: Date | string): string {
    const value = typeof date === 'string' ? new Date(date) : date;
    return Number.isNaN(value.getTime()) ? '' : value.toISOString();
}
