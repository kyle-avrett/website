// @ts-check
import tailwindcss from '@tailwindcss/vite';
import compressor from 'astro-compressor';
import llms from 'astro-llms-md';
import expressiveCode from 'astro-expressive-code';
import pagefind from 'astro-pagefind';
import robotsTxt from 'astro-robots-txt';
import purgecss from 'astro-purgecss';
import { defineConfig, envField, fontProviders } from 'astro/config';
import mdx from '@astrojs/mdx';

import icon from 'astro-icon';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
    site: 'https://kyleavrett.com',

    vite: {
        plugins: [tailwindcss()],
    },

    env: {
        schema: {
            API_URL: envField.string({
                context: 'client',
                access: 'public',
            }),
        },
    },

    fonts: [
        {
            name: 'Inter',
            cssVariable: '--font-inter',
            provider: fontProviders.google(),
            weights: [400, 500, 600, 700],
            styles: ['normal'],
            subsets: ['latin'],
        },
    ],

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
                    'brand-bluesky',
                    'brand-facebook',
                    'brand-x',
                    'mail',
                    'link',
                    'rss',
                    'search',
                    'calendar',
                    'refresh',
                    'user',
                    'arrow-big-left',
                    'arrow-up-right',
                ],
            },
        }),
        sitemap({
            filter: (page) => !page.endsWith('/search/'),
            xslURL: '/sitemap.xsl',
        }),
        robotsTxt(),
        llms({
            name: 'Kyle Avrett',
            description: 'Kyle Avrett website.',
        }),
        pagefind(),
        purgecss(),
        compressor(),
    ],

    build: {
        inlineStylesheets: 'always',
    },
});
