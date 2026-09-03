/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
    readonly SITE_URL?: string;
    readonly API_URL?: string;
    readonly CI_SKIP_CONTENT_COLLECTIONS?: string;
    readonly CI_SKIP_RSS_SITEMAP?: string;
    readonly ANALYTICS_SCRIPT?: string;
    readonly ANALYTICS_SITE_ID?: string;
    readonly PUBLIC_GISCUS_ENABLED?: string;
    readonly PUBLIC_GISCUS_REPO?: string;
    readonly PUBLIC_GISCUS_REPO_ID?: string;
    readonly PUBLIC_GISCUS_CATEGORY?: string;
    readonly PUBLIC_GISCUS_CATEGORY_ID?: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}
