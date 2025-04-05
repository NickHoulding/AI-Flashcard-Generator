// Theme toggle functionality for the header button.
export function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    setTheme(newTheme);
}

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

    setTheme(currentTheme);
}

// Set initial theme when the page loads.
window.addEventListener('DOMContentLoaded', () => {
    setInitialTheme();
});