exports.data = {
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    let posts = data.collections.posts.sort((a, b) => b.data.date - a.data.date);
    
    return `
    <ul id='blog-posts'>
      ${posts.map(blog =>
        `<li>
          <time>${blog.date.toLocaleDateString('en-UK', data.myProject.dateStringOptions)}</time>
          <a href="${blog.url}"><h2>${blog.data.title}</h2></a>
          <p>${this.excerpt(blog)}</p>
        </li>`
        ).join("\n")}
    </ul>`;
};