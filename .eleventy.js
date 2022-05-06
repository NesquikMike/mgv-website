// We do this so that we can have more control of the HTML output of our markdown
// Link: https://giuliachiola.dev/posts/add-html-classes-to-11ty-markdown-content/
const markdownIt = require('markdown-it')
const markdownItAttrs = require('markdown-it-attrs')
const markdownItFootnote = require('markdown-it-footnote')

const striptags = require("striptags");

const markdownItOptions = {
    html: true,
    breaks: true,
    linkify: true
}

const markdownLib = markdownIt(markdownItOptions).use(markdownItAttrs).use(markdownItFootnote)

module.exports = function(eleventyConfig) {

    // This is necessary so that the assets are served and built by eleventy
    // as detailed here: https://michaelsoolee.com/add-css-11ty/
    eleventyConfig.addPassthroughCopy('assets');
    eleventyConfig.setLibrary('md', markdownLib);

    // This is used to demark the excerpts of the blog post that are used to
    // preview the blog post on the home page.
    // This is detailed here: https://keepinguptodate.com/pages/2019/06/creating-blog-with-eleventy/
    eleventyConfig.addShortcode("excerpt", (article) => extractExcerpt(article));

}

// This is used to demark the excerpts of the blog post that are used to
// preview the blog post on the home page.
// This is detailed here: https://www.jonathanyeong.com/garden/excerpts-with-eleventy/
function extractExcerpt(article) {
  if (!article.hasOwnProperty("templateContent")) {
    console.warn(
      'Failed to extract excerpt: Document has no property "templateContent".'
    );
    return null;
  }

  let excerpt = null;
  const content = article.templateContent;

  excerpt = striptags(content)
    .substring(0, 300) // Cap at 200 characters
    .replace(/^\s+|\s+$|\s+(?=\s)/g, "")
    .trim()
    .concat("...");
  return excerpt;
}