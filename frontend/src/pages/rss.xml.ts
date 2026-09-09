import type { APIRoute } from 'astro';
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async (context) => {
    const posts = await getCollection('blog');

    return rss({
        title: 'Kyle Avrett\'s Blog',
        description:
            'Software, product, and engineering leadership posts by Kyle Avrett',
        site: context.site!,
        items: posts
            .filter((post) => !post.data.draft)
            .map((post) => ({
                title: post.data.title,
                description: post.data.description,
                published: post.data.published,
                link: `/blog/${post.id}/`,
            })),
        stylesheet: '/rss.xsl',
        customData: '<language>en-us</language>',
    });
};
