<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" />

    <xsl:template match="/rss/channel">
        <html lang="en">
            <head>
                <title><xsl:value-of select="title" /></title>
                <style>
                    body { font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 64rem; padding: 0 1rem; line-height: 1.5; }
                    a { color: currentColor; }
                    article { border-top: 1px solid #ddd; padding: 1rem 0; }
                    time { color: #666; }
                </style>
            </head>
            <body>
                <main>
                    <h1><xsl:value-of select="title" /></h1>
                    <p><xsl:value-of select="description" /></p>
                    <xsl:for-each select="item">
                        <article>
                            <h2><a href="{link}"><xsl:value-of select="title" /></a></h2>
                            <time><xsl:value-of select="published" /></time>
                            <p><xsl:value-of select="description" /></p>
                        </article>
                    </xsl:for-each>
                </main>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
