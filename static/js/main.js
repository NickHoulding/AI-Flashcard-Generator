// Main JavaScript file to handle global functionality.
import { toggleModal } from "./modal.js";
import { addFile } from "./file.js";
import { sendMessage } from "./query.js";
import { loadFiles } from "./file.js";
import { setTheme, toggleTheme } from './theme.js';

window.sendMessage = sendMessage;
window.toggleTheme = toggleTheme;
window.toggleModal = toggleModal;
window.setTheme = setTheme;
window.addFile = addFile;

loadFiles();