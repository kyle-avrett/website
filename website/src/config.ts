import process from 'node:process';
import avatarImg from './assets/images/site/avatar.png';
import ogDefaultImg from './assets/images/site/og-default.png';
import type { GiscusConfig, NavItem, SiteConfig, SocialLink } from './types/config';

// site images
export const SITE_IMAGES = {
    avatar: avatarImg,
    ogDefault: ogDefaultImg,
} as const;

// socials
const GITHUB_HANDLE = import.meta.env.PUBLIC_GITHUB_HANDLE ?? '';
const GITHUB_REPO = import.meta.env.PUBLIC_GITHUB_REPO ?? '';
const TWITTER_HANDLE = import.meta.env.PUBLIC_TWITTER_HANDLE ?? '';
const CONTACT_EMAIL = import.meta.env.PUBLIC_CONTACT_EMAIL ?? '';

// website repo
export const REPO = {
    handle: GITHUB_HANDLE,
    name: GITHUB_REPO,
    url: GITHUB_HANDLE
        ? `https://github.com/${GITHUB_HANDLE}/${GITHUB_REPO}`
        : 'https://github.com',
} as const;

// site config
export const SITE: SiteConfig = {
    title: 'Kyle Avrett',
    description: 'Hands-on CTO / Head of Engineering',
    author: {
        name: 'Kyle Avrett',
        avatar: avatarImg,
        bio: 'Hands-on CTO / Head of Engineering',
    },
    defaultOgImage: ogDefaultImg.src,
    postsPerPage: 12,
    isoDates: false,
    showFeaturedImages: true,
    boxedArticles: true,
    dynamicPostCardHeight: false,
    autoOgImage: true,
    url: process.env.SITE_URL || 'https://kyleavrett.com',
};

// navbar
export const NAV: readonly NavItem[] = [
    { label: 'Posts', href: '/', icon: 'lucide:newspaper' },
    { label: 'Projects', href: '/categories', icon: 'lucide:folder' },
    { label: 'About', href: '/about', icon: 'lucide:info' },
] as const;

// socials
export const SOCIALS: readonly SocialLink[] = [
    GITHUB_HANDLE && {
        label: 'GitHub',
        href: `https://github.com/${GITHUB_HANDLE}`,
        icon: 'simple-icons:github',
    },
    TWITTER_HANDLE && {
        label: 'Twitter',
        href: `https://x.com/${TWITTER_HANDLE}`,
        icon: 'simple-icons:x',
    },
    CONTACT_EMAIL && {
        label: 'Email',
        href: `mailto:${CONTACT_EMAIL}`,
        icon: 'lucide:mail',
    },
    { label: 'RSS', href: '/rss.xml', icon: 'lucide:rss' },
].filter(Boolean) as SocialLink[];

// comments
export const GISCUS: GiscusConfig = {
    enabled: (import.meta.env.PUBLIC_GISCUS_ENABLED ?? 'false') === 'true',
    repo: import.meta.env.PUBLIC_GISCUS_REPO ?? '',
    repoId: import.meta.env.PUBLIC_GISCUS_REPO_ID ?? '',
    category: import.meta.env.PUBLIC_GISCUS_CATEGORY ?? 'Announcements',
    categoryId: import.meta.env.PUBLIC_GISCUS_CATEGORY_ID ?? '',
    mapping: 'pathname',
    strict: '0',
    reactionsEnabled: '1',
    emitMetadata: '0',
    inputPosition: 'bottom',
    loading: 'lazy',
};

// pagefind
export const PAGEFIND = {
    bundlePath: '/_pagefind/',
    pageSize: 12,
} as const;
