/** Prefix an absolute path with Astro's configured base path. */
export function withBase(path: string): string {
    const base = (import.meta.env.BASE_URL ?? '/').replace(/\/+$/, '');
    if (!path || !path.startsWith('/') || !base) return path;
    if (path === base || path.startsWith(`${base}/`)) return path;
    return `${base}${path}`;
}
