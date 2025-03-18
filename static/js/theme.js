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

// Sets initial theme to dark.
function setInitialTheme() {
    const root = document.documentElement;
    const currentTheme = 'dark';
    root.setAttribute('data-theme', currentTheme);
}

// Set initial theme when the page loads.
window.addEventListener('DOMContentLoaded', () => {
    setInitialTheme();
});
