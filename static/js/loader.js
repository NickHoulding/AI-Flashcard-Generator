class Loader extends HTMLElement {
    // Construct the custom element.
    constructor() {
        super();

        // Create shadow root and define element structure.
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <link rel="stylesheet" href="/static/css/loader.css">
            <div class="loader"></div>
        `;
    }
}

// Define the custom element.
customElements.define('loader-custom', Loader);