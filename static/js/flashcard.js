export class Flashcard extends HTMLElement {
    // Define element attributes that can be observed.
    static get observedAttributes() {
        return [
            'number',
            'question',
            'answer'
        ];
    }

    // Construct the custom element.
    constructor() {
        super();

        // Set default values.
        if (!this.hasAttribute('number')) {
            this.setAttribute('number', '-');
        }
        if (!this.hasAttribute('question')) {
            this.setAttribute('question', '');
        }
        if (!this.hasAttribute('answer')) {
            this.setAttribute('answer', '');
        }
        
        // Create shadow root and define element structure.
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <link rel="stylesheet" href="/static/css/flashcard.css">
            <div class="flashcard">
                <div class="info">
                    <div class="indicator" id="indicator">${this.getAttribute('number')}</div>
                    <button class="delete-card">
                        <svg 
                            fill="currentColor" 
                            height="24" 
                            viewBox="0 0 24 24" 
                            width="24" 
                            xmlns="http://www.w3.org/2000/svg">
                            <path d="M21.5 6C21.5 6.51284 21.114 6.93551 20.6166 6.99327L20.5 7H19.6553L18.4239 19.5192C18.2854 20.9269 17.1016 22 15.6871 22H8.31293C6.8984 22 5.7146 20.9269 5.57614 19.5192L4.34474 7H3.5C2.94772 7 2.5 6.55228 2.5 6C2.5 5.44772 2.94772 5 3.5 5H8.5C8.5 3.067 10.067 1.5 12 1.5C13.933 1.5 15.5 3.067 15.5 5H20.5C21.0523 5 21.5 5.44772 21.5 6ZM14.25 9.25C13.8703 9.25 13.5565 9.53215 13.5068 9.89823L13.5 10V17L13.5068 17.1018C13.5565 17.4678 13.8703 17.75 14.25 17.75C14.6297 17.75 14.9435 17.4678 14.9932 17.1018L15 17V10L14.9932 9.89823C14.9435 9.53215 14.6297 9.25 14.25 9.25ZM9.75 9.25C9.3703 9.25 9.05651 9.53215 9.00685 9.89823L9 10V17L9.00685 17.1018C9.05651 17.4678 9.3703 17.75 9.75 17.75C10.1297 17.75 10.4435 17.4678 10.4932 17.1018L10.5 17V10L10.4932 9.89823C10.4435 9.53215 10.1297 9.25 9.75 9.25ZM12 3.5C11.1716 3.5 10.5 4.17157 10.5 5H13.5C13.5 4.17157 12.8284 3.5 12 3.5Z"/>
                        </svg>
                    </button>
                </div>
                <div class="text">
                    <textarea 
                        name="question" 
                        id="question" 
                        class="question" 
                        placeholder="Question">${this.getAttribute('question') || ''}</textarea>
                    <textarea 
                        name="answer" 
                        id="answer" 
                        class="answer" 
                        placeholder="Answer">${this.getAttribute('answer') || ''}</textarea>
                </div>
            </div>
        `;
    }

    // Delete the flashcard element when clicked.
    connectedCallback() {
        this.shadowRoot
        .querySelector('.delete-card')
        .addEventListener(
            'click', 
            () => this.deleteCard()
        );
    }

    // Removes event listener when element is deleted.
    disconnectedCallback() {
        this.shadowRoot
        .querySelector('.delete-card')
        .removeEventListener(
            'click', 
            () => this.deleteCard()
        );
    }

    // Implementation of the deleteCard method
    deleteCard() {
        this.remove();
    }

    // Updates the element when an attribute changes.
    attributeChangedCallback(name, oldVal, newVal) {
        if (oldVal !== newVal) {
            this[name] = newVal;
            
            // Update DOM elements if they exist
            if (this.shadowRoot) {
                if (name === 'number') {
                    const indicator = this.shadowRoot.querySelector('#indicator');
                    if (indicator) {
                        indicator.textContent = `${newVal}`;
                    }
                } else if (name === 'question') {
                    const question = this.shadowRoot.querySelector('#question');
                    if (question) {
                        question.value = newVal || '';
                    }
                } else if (name === 'answer') {
                    const answer = this.shadowRoot.querySelector('#answer');
                    if (answer) {
                        answer.value = newVal || '';
                    }
                }
            }
        }
    }
}

// Define the custom element.
customElements.define('flash-card', Flashcard);