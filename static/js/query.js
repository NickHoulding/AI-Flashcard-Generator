async function sendMessage() {
    const textbox = document.getElementById('user-input');
    const message = textbox.value;
    textbox.value = '';

    const response = await fetch('/send-message', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });
    
    if (response.ok) {
        const data = await response.json();
        alert(data.response);
    } else {
        alert('Error sending message');
    }
}