module.exports = function(data) {
    return `
<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${data.title ? `${data.title} | ${data.metadata.title}` : `${data.metadata.title}`}</title>
  <script type="module">
    document.documentElement.classList.remove('no-js');
    document.documentElement.classList.add('js');
  </script>
  <link rel="stylesheet" href="/assets/css/styles.css">
  <link rel="stylesheet" href="/assets/css/print.css" media="print">
  <meta name="description" content="${this.postDescription(data) ? `${this.postDescription(data)}` : `${data.metadata.description}`}" >

  <meta property="og:title" content="${data.title ? `${data.title} | ${data.metadata.title}` : `${data.metadata.title}`}" >
  <meta proprty="og:description" content="${this.postDescription(data) ? `${this.postDescription(data)}` : `${data.metadata.description}`}" >
  <meta property="og:image" content="" >
  <meta property="og:locale" content="en_GB" >
  <meta property="og:type" content="${data.og_type}" >
  <meta property="og:url" content="${data.metadata.url}${data.page.url}" >
  <meta name="twitter:card" content="summary_large_image">

  <meta name="theme-color" content="#A9978E">

  <link rel="icon" href="/favicon.ico">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">

  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/my.webmanifest">

  <link rel="canonical" href="${data.metadata.url}${data.page.url}">

  <script src="assets/js/script.js" type="module"></script>
  <script data-goatcounter="https://michaelgvcouk.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
</head>
<body>
  <header>
    <h1><a class="nav-link" href="/">Michael Gomes Vieira</a></h1>
    <input type="checkbox" id="nav-check"/>
    <div class="nav-btn">
      <label class="hamburger-button" for="nav-check">
        <div></div>
        <div></div>
        <div></div>
      </label>
    </div>
    <ul class="list-nav">
      <li><a class="nav-link" href="/about/" target="_blank rel=noopener&quot;">About</a></li>
      <li><a class="nav-link" href="/projects/" target="_blank rel=noopener&quot;">Projects</a></li>
      <li><a class="nav-link" href="/assets/michaelgv_cv.pdf" download>CV</a></li>
      <li><a class="nav-link" href="https://github.com/NesquikMike" target="_blank rel=noopener&quot;">GitHub</a></li>
      <li><a class="nav-link" href='https://www.linkedin.com/in/michael-gomes-vieira-92865129/' target="_blank rel=noopener&quot;">LinkedIn</a></li>
    </ul>
  </header>
  <main>
    <div class="data-content">
      ${data.content}
    </div>
  </main>
</body>
</html>
    `;
};