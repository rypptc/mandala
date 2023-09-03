const lightSchemeIcon = document.querySelector('link#light-scheme-icon');
const darkSchemeIcon = document.querySelector('link#dark-scheme-icon');

const matcher = window.matchMedia('(prefers-color-scheme: dark)');
matcher.addListener(onUpdate);
onUpdate(); // Call it initially to set the correct favicon on page load

function onUpdate() {
  if (matcher.matches) {
    lightSchemeIcon.remove();
    document.head.append(darkSchemeIcon);
  } else {
    document.head.append(lightSchemeIcon);
    darkSchemeIcon.remove();
  }
}
