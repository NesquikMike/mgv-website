exports.data = {
    // title: "Blog",
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    return `
<ul>
  ${data.collections.posts.map(blog =>
    `<li>
      <a href="${blog.url}">${blog.data.title}</a>
      <p>Preview</p>
      <p>${blog.date}</p>
    </li>`
    ).join("\n")}
</ul>
<p>poop</p>
    `;
};