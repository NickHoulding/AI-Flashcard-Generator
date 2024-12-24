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
        typeResponse(data, responseElement);
    } else {
        alert('Error sending message');
    }
}

function typeResponse(data, element) {
    const text = data.message.content + "\n" + data.message.sources;
    let i = 0;

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, 5);
        }
    }

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