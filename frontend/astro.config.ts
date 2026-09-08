// @ts-check
import tailwindcss from '@tailwindcss/vite';
import compressor from 'astro-compressor';
import { astroFont } from 'astro-font/integration';
import llms from 'astro-llms-md';
import expressiveCode from 'astro-expressive-code';
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

    vite: {
        plugins: [tailwindcss()],
    },

    integrations: [
        expressiveCode({
            themes: ['one-light'],
            styleOverrides: {
                borderRadius: '0',
                frames: {
                    frameBoxShadowCssValue: 'none',
                },
            },
        }),
        mdx(),
        icon({
            include: {
                tabler: [
                    'brand-github',
                    'brand-linkedin',
                    'brand-x',
                    'mail',
                    'rss',
                    'search',
                    'calendar',
                    'refresh',
                    'user',
                    'arrow-big-left',
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
