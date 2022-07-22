exports.data = {
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    return `
    <ul id='blog-posts'>
      ${data.collections.posts.reverse().map(blog =>
        `<li>
          <time>${blog.date.toLocaleDateString('en-UK', data.myProject.dateStringOptions)}</time>
          <a href="${blog.url}"><h2>${blog.data.title}</h2></a>
          <p>${this.excerpt(blog)}</p>
        </li>`
        ).join("\n")}
    </ul>`;
};