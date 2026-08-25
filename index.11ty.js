exports.data = {
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    let posts = data.collections.posts.sort((a, b) => b.data.date - a.data.date);
    
    return `
    <p class="site-intro">I live in London and work as a data scientist at <a href="https://wayve.ai/" target="_blank" rel="noopener">Wayve</a>. I write about copying, culture, and other ordinary things that everyone treats as weather.</p>
    <p><a href="/feed.xml">Subscribe via RSS</a></p>
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