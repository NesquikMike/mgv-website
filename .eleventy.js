// We do this so that we can have more control of the HTML output of our markdown
// Link: https://giuliachiola.dev/posts/add-html-classes-to-11ty-markdown-content/
const markdownIt = require('markdown-it')
const markdownItAttrs = require('markdown-it-attrs')

const markdownItOptions = {
    html: true,
    breaks: true,
    linkify: true
}

const markdownLib = markdownIt(markdownItOptions).use(markdownItAttrs)

module.exports = function(eleventyConfig) {

    // This is necessary so that the assets are served and built by eleventy
    // as detailed here: https://michaelsoolee.com/add-css-11ty/
    eleventyConfig.addPassthroughCopy('assets');
    eleventyConfig.setLibrary('md', markdownLib);
}