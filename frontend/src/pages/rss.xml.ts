import rss from '@astrojs/rss';
import type { APIRoute } from 'astro';
import { SITE } from '~/config';
import { getPosts, postPath } from '~/utils/posts';

export const GET: APIRoute = async (context) => {
    const base = import.meta.env.BASE_URL.replace(/\/$/, '');
    const siteWithBase = `${context.site?.origin ?? SITE.url.replace(/\/$/, '')}${base}`;
    if (import.meta.env.CI_SKIP_RSS_SITEMAP === 'true') {
        return rss({
            title: SITE.title,
            description: SITE.description,
            site: siteWithBase,
            trailingSlash: false,
            stylesheet: `${base}/rss/styles.xsl`,
            items: [],
            customData: `<language>en-us</language>`,
        });
    }

    const posts = await getPosts();
    return rss({
        title: SITE.title,
        description: SITE.description,
        site: siteWithBase,
        trailingSlash: false,
        stylesheet: `${base}/rss/styles.xsl`,
        items: posts.map((post) => ({
            title: post.data.title,
            pubDate: post.data.pubDate,
            description: post.data.description,
            link: postPath(post),
            categories: [...post.data.tags, ...post.data.categories],
        })),
        customData: `<language>en-us</language>`,
    });
};
