export function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', newTheme);
}

function setInitialTheme() {
    const root = document.documentElement;
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const currentTheme = prefersDarkScheme ? 'dark' : 'light';
    root.setAttribute('data-theme', currentTheme);
}

window.addEventListener('DOMContentLoaded', () => {
    setInitialTheme();
});