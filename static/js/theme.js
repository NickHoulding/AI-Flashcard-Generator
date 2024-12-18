export function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    if (newTheme === 'dark') {
        root.style.setProperty('--theme-button-rotate', '180deg');
    } else {
        root.style.setProperty('--theme-button-rotate', '0deg');
    }

    root.setAttribute('data-theme', newTheme);
}

function setInitialTheme() {
    const root = document.documentElement;
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const currentTheme = prefersDarkScheme ? 'dark' : 'light';
    root.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'dark') {
        root.style.setProperty('--theme-button-rotate', '180deg');
    } else {
        root.style.setProperty('--theme-button-rotate', '0deg');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    setInitialTheme();
});