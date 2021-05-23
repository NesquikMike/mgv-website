module.exports = function(data) {
    return `
<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Michael Gomes Vieira</title>
  <script type="module">
    document.documentElement.classList.remove('no-js');
    document.documentElement.classList.add('js');
  </script>
  <link rel="stylesheet" href="./assets/css/styles.css">
  <link rel="stylesheet" href="./assets.css/print.css" media="print">
  <meta name="description" content="${data.metadata.description}" >

  <meta property="og:title" content="${data.metadata.title}" >
  <meta proprty="og:description" content="${data.metadata.description}" >
  <meta property="og:image" content="" >
  <meta property="og:locale" content="en_GB" >
  <meta property="og:type" content="${data.og_type}" >
  <meta property="og:url" content="${data.metadata.url}${data.page.url}" >
  <meta name="twitter:card" content="summary_large_image">

  <meta name="theme-color" content="#FF00FF">

  <link rel="icon" href="/favicon.ico">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">

  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/my.webmanifest">

  <link rel="canonical" href="${data.metadata.url}${data.page.url}">

  <script src="assets/js/script.js" type="module"></script>
</head>
<body>
  <header>
    <h1>Michael Gomes Vieira</h1>
    <nav>
      <input type="checkbox" id="nav-check"/>
      <div class="nav-btn">
        <label for="nav-check">
          <img src="assets/img/hamburger_button.png" height="20" width="20" id="menu-burger-button">
        </label>
      </div>
      <ul class="list-nav">
        <a href="#portfolio-section"><li class='nav-button'>Portfolio</li></a>
        <a href="#about-section"><li class="nav-button">About Me</li></a>
        <a href='https://medium.com/@b.archibald'><li class="nav-button">Blog</li></a>
        <a href='mailto:b.archibald2020@gmail.com'><li class="nav-button">Contact</li></a>
        <a href="assets/beth_archibald_cv.pdf" download><li class="nav-button">CV</li></a>
      </ul>
    </nav> 
  </header>
  <main>
    <h1>${data.title}</h1>
    ${data.content}
  </main>
  <footer>Site Footer</footer>
</body>
</html>
    `;
};