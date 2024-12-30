// Toggle dark/light app theme.
export function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute(
        'data-theme'
    );
    const newTheme = currentTheme === 'dark' 
        ? 'light' 
        : 'dark';
    root.setAttribute('data-theme', newTheme);
}

// Set initial theme based on user preference.
function setInitialTheme() {
    const root = document.documentElement;
    const prefersDarkScheme = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;
    const currentTheme = prefersDarkScheme 
        ? 'dark' 
        : 'light';
    root.setAttribute('data-theme', currentTheme);
}

// Set initial theme when the page loads.
window.addEventListener('DOMContentLoaded', () => {
    setInitialTheme();
});