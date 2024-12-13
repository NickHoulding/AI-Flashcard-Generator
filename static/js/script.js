let visible = false;

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('hamburger');
    const root = document.documentElement;

    if (visible) {
        sidebar.classList.add('hidden');
        root.style.setProperty('--logo-left-margin', '50px');
        root.style.setProperty('--sidebar-pos', '250px');
        root.style.setProperty('--content-width', 'calc(100%)');
        hamburger.classList.remove('hidden');
    } else {
        sidebar.classList.remove('hidden');
        root.style.setProperty('--logo-left-margin', '270px');
        root.style.setProperty('--sidebar-pos', '0px');
        root.style.setProperty('--content-width', 'calc(100% - 250px)');
        root.style.setProperty('--hamburger-opacity', '0%');
        hamburger.classList.add('hidden');        
    }

    visible = !visible;
}

function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    const icon = document.getElementById('theme');
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

    const icon = document.getElementById('theme');
    if (currentTheme === 'dark') {
        root.style.setProperty('--theme-button-rotate', '180deg');
    } else {
        root.style.setProperty('--theme-button-rotate', '0deg');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    setInitialTheme();
});

async function sendMessage() {
    const textbox = document.getElementById('user-input');
    const message = textbox.value;
    textbox.value = '';

    const response = await fetch('/send-message', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });
    
    if (response.ok) {
        const data = await response.json();
        alert(data.response);
    } else {
        alert('Error sending message');
    }
}