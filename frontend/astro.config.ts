// @ts-check
import tailwindcss from '@tailwindcss/vite';
import compressor from 'astro-compressor';
import { astroFont } from 'astro-font/integration';
import llms from 'astro-llms-md';
import pagefind from 'astro-pagefind';
import robotsTxt from 'astro-robots-txt';
import purgecss from 'astro-purgecss';
import { defineConfig } from 'astro/config';

import mdx from '@astrojs/mdx';

import icon from 'astro-icon';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
    site: 'http://localhost:4321',

    markdown: {
        syntaxHighlight: 'shiki',
    },

    vite: {
        plugins: [tailwindcss()],
    },

    integrations: [
        mdx(),
        icon({
            include: {
                tabler: [
                    'search',
                    'rss',
                    'mail',
                    'brand-linkedin',
                    'brand-github',
                    'brand-x',
                ],
            },
        }),
        sitemap({
            xslURL: '/sitemap.xsl',
        }),
        robotsTxt(),
        llms({
            name: 'Kyle Avrett',
            description: 'Kyle Avrett website.',
        }),
        pagefind(),
        astroFont(),
        purgecss(),
        compressor(),
    ],

    build: {
        inlineStylesheets: 'never',
    },
});
