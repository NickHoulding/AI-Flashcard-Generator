// Theme management for the application.
export function setTheme(val) {
    const root = document.documentElement;
    root.setAttribute('data-theme', val);
    localStorage.setItem('theme', val);
}

// Sets initial theme based on saved preference or defaults to dark.
function setInitialTheme() {
    const root = document.documentElement;
    const currentTheme = localStorage.getItem('theme') || 'dark';
    const themeButton = document.getElementById('theme-dropdown');

    themeButton.value = currentTheme;
    setTheme(currentTheme);
    localStorage.setItem('theme', currentTheme);
}

// Set initial theme when the page loads.
window.addEventListener('DOMContentLoaded', () => {
    setInitialTheme();
});