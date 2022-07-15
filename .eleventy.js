// Adds dev functionality for derving 404 pages. More info can be found at this link:
// https://www.11ty.dev/docs/quicktips/not-found/
const fs = require("fs");
const NOT_FOUND_PATH = "_site/404.html";

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

    eleventyConfig.setUseGitIgnore(false);

    // To serve 404 page in dev. Code taken from here:
    // https://www.11ty.dev/docs/quicktips/not-found/ 
    eleventyConfig.setBrowserSyncConfig({
      callbacks: {
        ready: function(err, bs) {
  
          bs.addMiddleware("*", (req, res) => {
            if (!fs.existsSync(NOT_FOUND_PATH)) {
              throw new Error(`Expected a \`${NOT_FOUND_PATH}\` file but could not find one. Did you create a 404.html template?`);
            }
  
            const content_404 = fs.readFileSync(NOT_FOUND_PATH);
            // Add 404 http status code in request header.
            res.writeHead(404, { "Content-Type": "text/html; charset=UTF-8" });
            // Provides the 404 content without redirect.
            res.write(content_404);
            res.end();
          });
        }
      }
    }); 
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
    .substring(0, 300) // Cap at 300 characters
    .replace(/^\s+|\s+$|\s+(?=\s)/g, "")
    .trim()
    .concat("...");
  return excerpt;
}