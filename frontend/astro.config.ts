// @ts-check
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'astro/config';

import mdx from '@astrojs/mdx';

import icon from 'astro-icon';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
    site: 'https://example.com',

    markdown: {
        syntaxHighlight: 'shiki',
    },

    vite: {
        plugins: [tailwindcss()],
    },

    integrations: [mdx(), icon(), sitemap()],
});
