// Handle user input and send to server for processing.
export async function sendMessage() {
    // Get user input and chat elements.
    const textbox = document.getElementById(
        'user-input'
    );
    const chat = document.getElementById('chat');
    const message = textbox.value;
    textbox.value = '';

    // Create user message element.
    const messageElement = document.createElement(
        'div'
    );
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
        
        // Create and insert AI response element into chat.
        const responseElement = document.createElement(
            'div'
        );
        responseElement.className = 'ai-response';
        chat.appendChild(responseElement);

        // Type out AI response content.
        const htmlContent = 
            data.message.content 
            + data.message.sources;
        typeResponse(
            htmlContent, 
            responseElement
        );
    } else {
        alert('Error sending message');
    }
}

// Animation effect typing out AI response.
function typeResponse(htmlContent, element) {
    let i = 0;
    const interval = 5;

    // Recursive function to type out content.
    const type = () => {
        if (i <= htmlContent.length) {
            element.innerHTML = htmlContent.slice(0, i);
            i++;
            setTimeout(type, interval);
        }
    };

    type();
}

// Send message when user presses Enter key.
document.addEventListener('DOMContentLoaded', function() {
    // Get input text area and listen for Enter key.
    document.getElementById(
        'user-input'
    ).addEventListener(
        'keydown', function(event) {
            // Prevent default form submission.
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });
});