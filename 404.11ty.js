exports.data = {
    permalink: '404.html',
    layout: "base-layout.11ty.js",
    eleventyExcludeFromCollections: true
};

exports.render = function(data) {
    return `
      <div class='four04'>
        <h1>Ooops! You're on the 404 Page 😽</h1>
        <p>You can find your way back to my homepage <a href='/'>here</a> 👈</p>
        <p>Or if you think this is a 🪲 you can <a href='https://github.com/NesquikMike/mgv-website/issues'>log an issue here!</a></p>
      <div>
    `;
};