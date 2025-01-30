import { toggleSidebar } from "./sidebar.js";
import { toggleTheme } from "./theme.js";
import { toggleModal } from "./modal.js";
import { addFile } from "./file.js";
import { sendMessage } from "./query.js";

// Assign functions to global window to access from html.
window.sendMessage = sendMessage;
window.toggleTheme = toggleTheme;
window.toggleSidebar = toggleSidebar;
window.toggleModal = toggleModal;
window.addFile = addFile;