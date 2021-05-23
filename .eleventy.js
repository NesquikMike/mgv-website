module.exports = function(eleventyConfig) {

    // This is necessary so that the assets are served and built by eleventy
    // as detailed here: https://michaelsoolee.com/add-css-11ty/
    eleventyConfig.addPassthroughCopy('assets');
}