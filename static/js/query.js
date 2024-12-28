export async function sendMessage() {
    const textbox = document.getElementById('user-input');
    const chat = document.getElementById('chat');
    const message = textbox.value;
    textbox.value = '';

    const messageElement = document.createElement('div');
    messageElement.className = 'user-message';
    messageElement.textContent = message;

    if (messageElement.textContent.trim() === '') {
        return;
    }
    
    chat.appendChild(messageElement);

    const response = await fetch('/send-message', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });
    
    if (response.ok) {
        const data = await response.json();
        
        const responseElement = document.createElement('div');
        responseElement.className = 'ai-response';
        chat.appendChild(responseElement);

        typeResponse(data.message.content + data.message.sources, responseElement);
    } else {
        alert('Error sending message');
    }
}

function typeResponse(htmlContent, element) {
    let i = 0;
    const interval = 5;

    const type = () => {
        if (i <= htmlContent.length) {
            element.innerHTML = htmlContent.slice(0, i);
            i++;
            setTimeout(type, interval);
        }
    };

    type();
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('user-input').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});