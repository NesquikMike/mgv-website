exports.data = {
    title: "Projects",
    layout: "base-layout.11ty.js"
};

exports.render = function(data) {
    return `
      <h1>Projects</h1>
      <ul id="projects-list">
        ${
          data.collections.projects.map(project =>
            `<li>
              <a href="${project.data.url}" class="project-img-odd"><img src="${project.data.imgSrc}" alt="${project.data.imgAlt}"></img></a>
              <div class="project-info">
                <a class="project-title" href="${project.data.url}"><h2>${project.data.title}</h2></a>
                <div class="project-para">${project.templateContent}</div>
              </div>
              <a href="${project.data.url}" class="project-img-even"><img src="${project.data.imgSrc}" alt="${project.data.imgAlt}"></img></a>
            </li>`
          ).join("\n")
        }
      </ul>
    `;
    return `
`
};