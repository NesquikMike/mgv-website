exports.data = {
    layout: "base-layout.11ty.js",
    title: "Projects"
};

function projectThumb(project, side) {
    const img = `<img src="${project.data.imgSrc}" alt="${project.data.imgAlt}">`;
    const cls = `project-img project-${side}`;
    if (project.data.url) {
        return `<a href="${project.data.url}" class="${cls}">${img}</a>`;
    }
    return `<div class="${cls}">${img}</div>`;
}

function projectHeading(project) {
    if (project.data.url) {
        return `<a class="project-title" href="${project.data.url}"><h2>${project.data.title}</h2></a>`;
    }
    return `<h2>${project.data.title}</h2>`;
}

exports.render = function(data) {
    return `
      <h1>Projects</h1>
      <ul id="projects-list">
        ${
          data.collections.projects.sort((a, b) => a.data.weight - b.data.weight).map(project =>
            `<li>
              ${projectThumb(project, "odd")}
              <div class="project-info">
                ${projectHeading(project)}
                <div class="project-para">${project.templateContent}</div>
              </div>
              ${projectThumb(project, "even")}
            </li>`
          ).join("\n")
        }
      </ul>
    `;
};