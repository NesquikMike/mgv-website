exports.data = {
    title: "Blog Posts",
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    return `
<br>
<ul>
  ${data.collections.posts.map(blog =>
    `<li>
      <a href="${blog.url}">${blog.data.title}</a>
      <p>Preview</p>
      <p>${blog.date}</p>
    </li>`
    ).join("\n")}
</ul>
    `;
};