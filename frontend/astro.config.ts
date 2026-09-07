// @ts-check
import tailwindcss from '@tailwindcss/vite';
import compressor from 'astro-compressor';
import { astroFont } from 'astro-font/integration';
import llms from 'astro-llms-md';
import pagefind from 'astro-pagefind';
import robotsTxt from 'astro-robots-txt';
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

    integrations: [
        mdx(),
        icon(),
        sitemap(),
        robotsTxt(),
        llms({
            name: 'Kyle Avrett',
            description: 'Kyle Avrett website.',
        }),
        pagefind(),
        astroFont(),
        compressor(),
    ],
});
