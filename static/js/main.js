import { toggleTheme } from "./theme.js";
import { toggleModal } from "./modal.js";
import { addFile } from "./file.js";
import { sendMessage } from "./query.js";

window.sendMessage = sendMessage;
window.toggleTheme = toggleTheme;
window.toggleModal = toggleModal;
window.addFile = addFile;