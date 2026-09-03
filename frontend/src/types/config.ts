import type { ImageMetadata } from 'astro';

export interface SiteConfig {
    title: string;
    description: string;
    author: {
        name: string;
        url?: string;
        avatar?: string | ImageMetadata;
        bio?: string;
    };
    defaultOgImage: string;
    isoDates: boolean;
    showFeaturedImages: boolean;
    boxedArticles: boolean;
    dynamicPostCardHeight: boolean;
    autoOgImage: boolean;
    url: string;
}

export interface NavItem {
    label: string;
    href: string;
    /** Optional icon name (e.g. "home", "tags"). */
    icon?: string;
}

export interface SocialLink {
    label: string;
    href: string;
    icon: string;
}

export interface GiscusConfig {
    /** Master switch. */
    enabled: boolean;
    /** GitHub repo (e.g. `user/repo`). */
    repo: string;
    /** Repo ID (from giscus.app). */
    repoId: string;
    /** Discussion category. */
    category: string;
    /** Category ID. */
    categoryId: string;
    /** Discussion mapping strategy. */
    mapping: 'pathname' | 'url' | 'title' | 'og:title' | 'specific' | 'number';
    /** Strict matching. */
    strict: '0' | '1';
    /** Enable reactions on the main post. */
    reactionsEnabled: '0' | '1';
    /** Emit metadata events. */
    emitMetadata: '0' | '1';
    /** Comment input position. */
    inputPosition: 'top' | 'bottom';
    /** Lazy load. */
    loading: 'lazy' | 'eager';
}
