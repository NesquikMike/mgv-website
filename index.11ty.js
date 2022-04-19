exports.data = {
    title: "Blog Posts",
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    return `
<br>
<ul class='blog-posts'>
  ${data.collections.posts.map(blog =>
    `<li>
      <time>${blog.date.toLocaleDateString('en-UK', data.myProject.dateStringOptions)}</time>
      <a href="${blog.url}">${blog.data.title}</a>
      <p>${this.excerpt(blog)}</p>
    </li>`
    ).join("\n")}
</ul>
    `;
};