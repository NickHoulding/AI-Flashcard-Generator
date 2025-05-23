import { Flashcard } from './flashcard.js';

// Handle user input and send to server for processing.
export async function sendMessage() {
    // Get user input and chat elements.
    const textbox = document.getElementById('user-input');
    const chat = document.getElementById('chat');
    const message = textbox.value;
    textbox.value = '';

    // Create user message element.
    const messageElement = document.createElement('div');
    messageElement.className = 'user-message';
    messageElement.textContent = message;

    // Check for empty messages.
    if (messageElement.textContent.trim() === '') {
        return;
    }
    else {
        chat.appendChild(messageElement);
    }
    
    // Create and append loader.
    const loaderContainer = document.createElement('div');
    loaderContainer.className = 'loader-container';
    const loader = document.createElement('loader-custom');
    loaderContainer.appendChild(loader);
    chat.appendChild(loaderContainer);

    try {
        // Send message and await AI response.
        const response = await fetch('/send-message', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        
        if (chat.contains(loaderContainer)) {
            chat.removeChild(loaderContainer);
        }
        
        // Display AI response.
        if (response.ok) {
            const data = await response.json();
            
            const responseElement = document.createElement('div');
            responseElement.className = 'ai-response';
            chat.appendChild(responseElement);

            const flashcards = data.message.content;
            typeMessage(flashcards, responseElement);

            // TODO: Display sources.

        } else {
            alert('Error sending message');
        }
    } catch (error) {
        if (chat.contains(loaderContainer)) {
            chat.removeChild(loaderContainer);
        }
        alert('Error sending message: ' + error.message);
    }
}

// Typing animation effect for AI response.
function typeMessage(flashcards, element) {
    const delay = 50;

    for (let i = 0; i < flashcards.length; i++) {
        setTimeout(() => {
            const flashcard = new Flashcard();
            flashcard.setAttribute('number', i + 1);
            flashcard.setAttribute('question', flashcards[i].question);
            flashcard.setAttribute('answer', flashcards[i].answer);
            element.appendChild(flashcard);
        }, i * delay);
    }
}

// Send message when user presses Enter key.
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('user-input')
    .addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});