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

    // Send message and await AI response.
    const response = await fetch('/send-message', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });
    
    // Display AI response.
    if (response.ok) {
        const data = await response.json();
        
        const responseElement = document.createElement('div');
        responseElement.className = 'ai-response';
        chat.appendChild(responseElement);

        const flashcards = data.message.content;
        typeMessage(flashcards, responseElement);

        const sources = data.message.sources;
        const sourcesElement = document.createElement('div');
        sourcesElement.textContent = sources.join(', ');
        responseElement.appendChild(sourcesElement);
    } else {
        alert('Error sending message');
    }
}

// Typing animation effect for AI response.
function typeMessage(flashcards, element) {
    const delay = 50;

    for (let i = 0; i < flashcards.length; i++) {
        const line = flashcards[i].number + ": " + flashcards[i].question + " " + flashcards[i].answer;

        setTimeout(() => {
            const lineElement = document.createElement('div');
            lineElement.textContent = line;
            element.appendChild(lineElement);
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