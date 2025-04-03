class File extends HTMLElement {
    // Define element attributes that can be observed.
    static get observedAttributes() {
        return ['chatname'];
    }

    // Construct the custom element.
    constructor() {
        super();

        // Set default values.
        if (!this.hasAttribute('chatname')) {
            this.setAttribute('chatname', 'Unnamed Chat');
        }

        // Create shadow root and define element structure.
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <link rel="stylesheet" href="/static/css/chat.css">
            <div class="chat">
                <div class="chatname">Unnamed Chat</div>
                <button class="dots">
                    <svg 
                        fill="currentColor" 
                        height="24" 
                        viewBox="0 0 24 24" 
                        width="24" 
                        xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 12C8 13.1046 7.10457 14 6 14C4.89543 14 4 13.1046 4 12C4 10.8954 4.89543 10 6 10C7.10457 10 8 10.8954 8 12Z"/><path d="M14 12C14 13.1046 13.1046 14 12 14C10.8954 14 10 13.1046 10 12C10 10.8954 10.8954 10 12 10C13.1046 10 14 10.8954 14 12Z"/><path d="M18 14C19.1046 14 20 13.1046 20 12C20 10.8954 19.1046 10 18 10C16.8954 10 16 10.8954 16 12C16 13.1046 16.8954 14 18 14Z"/>
                    </svg>
                </button>
            </div>
        `;
    }
}

// Define the custom element.
customElements.define('chat-custom', File);