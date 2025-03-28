import { is_modal_active } from "./modal.js";

let visible = false;

export function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('logo-icon');
    const root = document.documentElement;

    if (visible) {
        sidebar.classList.add('hidden');
        hamburger.classList.remove('hidden');        
        root.style.setProperty('--logo-left-margin', '50px');
        root.style.setProperty('--sidebar-pos', '250px');
        root.style.setProperty('--content-width', 'calc(100%)');
        root.style.setProperty('--hamburger-opacity', '100%');
    } else {
        sidebar.classList.remove('hidden');
        hamburger.classList.add('hidden');
        root.style.setProperty('--logo-left-margin', '270px');
        root.style.setProperty('--sidebar-pos', '0px');
        root.style.setProperty('--content-width', 'calc(100% - 250px)');
        root.style.setProperty('--hamburger-opacity', '0%');
    }

    visible = !visible;
}

// Toggle the sidebar when CTRL + \ is pressed
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keydown', function(event) {
        
        if ((!is_modal_active()) &&
            (event.ctrlKey && event.key === '\\')
        ) {
            event.preventDefault();
            toggleSidebar();
        }
    });
});