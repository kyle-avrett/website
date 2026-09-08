import type { APIRoute } from 'astro';
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async (context) => {
    const posts = await getCollection('blog');

    return rss({
        title: 'Blog',
        description: 'Blog posts',
        site: context.site!,
        items: posts
            .filter((post) => !post.data.draft)
            .map((post) => ({
                title: post.data.title,
                description: post.data.description,
                pubDate: post.data.pubDate,
                link: `/blog/${post.id}/`,
            })),
        customData: '<language>en-us</language>',
    });
};
