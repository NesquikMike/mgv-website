exports.data = {
  permalink: "feed.xml",
  eleventyExcludeFromCollections: true
};

function escapeXml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function toAbsolute(html, baseUrl) {
  return html
    .replace(/(src|href)="\//g, `$1="${baseUrl}/`);
}

exports.render = function (data) {
  const baseUrl = data.metadata.url.replace(/\/$/, "");
  const posts = [...data.collections.posts].sort((a, b) => b.date - a.date);
  const latest = posts[0];
  const lastBuildDate = latest ? latest.date.toUTCString() : new Date().toUTCString();

  const items = posts.map((post) => {
    const url = `${baseUrl}${post.url}`;
    const html = toAbsolute(post.templateContent || "", baseUrl);
    return `    <item>
      <title>${escapeXml(post.data.title)}</title>
      <link>${escapeXml(url)}</link>
      <guid isPermaLink="true">${escapeXml(url)}</guid>
      <pubDate>${post.date.toUTCString()}</pubDate>
      <description><![CDATA[${html}]]></description>
    </item>`;
  }).join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${escapeXml(data.metadata.title)}</title>
    <link>${escapeXml(baseUrl)}/</link>
    <description>${escapeXml(data.metadata.description)}</description>
    <language>en-gb</language>
    <lastBuildDate>${lastBuildDate}</lastBuildDate>
    <atom:link href="${escapeXml(baseUrl)}/feed.xml" rel="self" type="application/rss+xml"/>
${items}
  </channel>
</rss>
`;
};
