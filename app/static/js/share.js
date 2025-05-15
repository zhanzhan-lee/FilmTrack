// Twemoji: render unicode emojis as images for consistent sidebar icons
// CDN: https://cdnjs.com/libraries/twemoji
document.addEventListener('DOMContentLoaded', () => {
  if (window.twemoji) {
    twemoji.parse(document.body, {
      folder: 'svg',
      ext: '.svg'
    });
  }
});
