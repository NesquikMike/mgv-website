exports.data = {
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    return `<article>
    <h1>${data.title}</h1>
    <time>${data.date.toLocaleDateString('en-UK', data.myProject.dateStringOptions)}</time>
    ${data.content}
    <script 
      src="https://utteranc.es/client.js"
      repo="NesquikMike/mgv-website"
      issue-term="title"
      label="💬"
      theme="github-light"
      crossorigin="anonymous"
      aync
    ></script>
  </article>`;
};