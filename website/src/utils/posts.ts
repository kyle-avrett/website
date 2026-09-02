/** Post collection, sorting, grouping, and URL helpers. */

import type { ImageMetadata } from 'astro';
import { getCollection, type CollectionEntry } from 'astro:content';

import { SITE } from '../config';
import { slugify } from './slugify';
import { withBase } from './url';

export type Post = CollectionEntry<'posts'>;

const isProd = import.meta.env.PROD;
const skipPostCollections = import.meta.env.CI_SKIP_CONTENT_COLLECTIONS === 'true';

export function postSlug(entry: Post): string {
    return entry.id.replace(/\.(md|mdx)$/i, '');
}

export function postPath(entry: Post): string {
    return withBase(`/posts/${postSlug(entry)}/`);
}

/** Sort posts by pin status, then publication date descending. */
export function sortPosts(posts: Post[]): Post[] {
    return [...posts].sort((a, b) => {
        if (a.data.pinned !== b.data.pinned) return a.data.pinned ? -1 : 1;
        return b.data.pubDate.valueOf() - a.data.pubDate.valueOf();
    });
}

/** Sort posts by publication date descending, ignoring pin status. */
export function sortPostsByDate(posts: Post[]): Post[] {
    return [...posts].sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export async function getPosts(): Promise<Post[]> {
    if (skipPostCollections) return [];
    const posts = await getCollection(
        'posts',
        (entry) => !(isProd && entry.data.draft) && !entry.data.unlisted,
    );
    return sortPosts(posts);
}

/** Unlisted posts still need generated routes for direct links. */
export async function getUnlistedPosts(): Promise<Post[]> {
    if (skipPostCollections) return [];
    const posts = await getCollection(
        'posts',
        (entry) => !(isProd && entry.data.draft) && entry.data.unlisted,
    );
    return sortPosts(posts);
}

export async function getTagsWithCount(): Promise<Array<{ name: string; count: number }>> {
    const posts = await getPosts();
    const counts = new Map<string, number>();
    for (const post of posts) {
        for (const tag of post.data.tags) counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
    return Array.from(counts, ([name, count]) => ({ name, count })).sort(
        (a, b) => b.count - a.count || a.name.localeCompare(b.name),
    );
}

export async function getCategoriesWithCount(): Promise<Array<{ name: string; count: number }>> {
    const posts = await getPosts();
    const counts = new Map<string, number>();
    for (const post of posts) {
        for (const category of post.data.categories) {
            counts.set(category, (counts.get(category) ?? 0) + 1);
        }
    }
    return Array.from(counts, ([name, count]) => ({ name, count })).sort(
        (a, b) => b.count - a.count || a.name.localeCompare(b.name),
    );
}

export function groupByYearMonth(posts: Post[]): Array<{
    year: number;
    months: Array<{ month: number; label: string; posts: Post[] }>;
}> {
    const buckets = new Map<number, Map<number, Post[]>>();
    for (const post of posts) {
        const year = post.data.pubDate.getFullYear();
        const month = post.data.pubDate.getMonth();
        if (!buckets.has(year)) buckets.set(year, new Map());
        const months = buckets.get(year)!;
        if (!months.has(month)) months.set(month, []);
        months.get(month)!.push(post);
    }
    const formatter = new Intl.DateTimeFormat('en-US', { month: 'long' });
    return Array.from(buckets.entries())
        .sort((a, b) => b[0] - a[0])
        .map(([year, months]) => ({
            year,
            months: Array.from(months.entries())
                .sort((a, b) => b[0] - a[0])
                .map(([month, posts]) => ({
                    month,
                    label: formatter.format(new Date(year, month, 1)),
                    posts,
                })),
        }));
}

export function shouldShowHero(post: Post): boolean {
    return Boolean(post.data.heroImage) && (post.data.showFeaturedImage ?? SITE.showFeaturedImages);
}

export function heroImageSrc(post: Post): string | undefined {
    const image = post.data.heroImage;
    const src =
        typeof image === 'string'
            ? image
            : image && typeof image === 'object' && 'src' in image
              ? image.src
              : undefined;
    return src?.startsWith('/') && !src.startsWith('//') ? withBase(src) : src;
}

export function heroImage(post: Post): ImageMetadata | string | undefined {
    const image = post.data.heroImage;
    if (typeof image === 'string') {
        return image.startsWith('/') && !image.startsWith('//') ? withBase(image) : image;
    }
    return image;
}

export { slugify } from './slugify';

export function tagPath(tag: string): string {
    return withBase(`/tags/${slugify(tag)}/`);
}

export function categoryPath(category: string): string {
    return withBase(`/categories/${slugify(category)}/`);
}
