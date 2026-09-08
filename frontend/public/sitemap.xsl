<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
    <xsl:output method="html" encoding="UTF-8" />

    <xsl:template match="/s:sitemapindex">
        <html lang="en">
            <head>
                <title>Sitemap Index</title>
                <xsl:call-template name="styles" />
            </head>
            <body>
                <main>
                    <h1>Sitemap Index</h1>
                    <ol>
                        <xsl:for-each select="s:sitemap">
                            <li><a href="{s:loc}"><xsl:value-of select="s:loc" /></a></li>
                        </xsl:for-each>
                    </ol>
                </main>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="/s:urlset">
        <html lang="en">
            <head>
                <title>Sitemap</title>
                <xsl:call-template name="styles" />
            </head>
            <body>
                <main>
                    <h1>Sitemap</h1>
                    <ol>
                        <xsl:for-each select="s:url">
                            <li><a href="{s:loc}"><xsl:value-of select="s:loc" /></a></li>
                        </xsl:for-each>
                    </ol>
                </main>
            </body>
        </html>
    </xsl:template>

    <xsl:template name="styles">
        <style>
            body { font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 64rem; padding: 0 1rem; line-height: 1.5; }
            a { color: currentColor; }
            li { margin: 0.5rem 0; }
        </style>
    </xsl:template>
</xsl:stylesheet>
