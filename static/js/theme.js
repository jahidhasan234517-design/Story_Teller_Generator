const root = document.documentElement;
const savedTheme = localStorage.getItem('news-dashboard-theme');
if (savedTheme) {
  root.setAttribute('data-theme', savedTheme);
}

const toggle = document.querySelector('.theme-toggle');
if (toggle) {
  toggle.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('news-dashboard-theme', next);
  });
}

const burger = document.querySelector('.mobile-toggle');
if (burger) {
  burger.addEventListener('click', () => {
    document.querySelector('.sidebar').classList.toggle('open');
  });
}
