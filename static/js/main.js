import { toggleSidebar } from "./sidebar.js";
import { toggleTheme } from "./theme.js";
import { toggleModal } from "./modal.js";
import { addFile } from "./file.js";
import { sendMessage } from "./query.js";
import { loadFiles } from "./file.js";

window.sendMessage = sendMessage;
window.toggleTheme = toggleTheme;
window.toggleSidebar = toggleSidebar;
window.toggleModal = toggleModal;
window.addFile = addFile;

loadFiles();