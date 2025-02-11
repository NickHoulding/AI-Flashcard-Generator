class File extends HTMLElement {
    // Define element attributes that can be observed.
    static get observedAttributes() {
        return ['filename'];
    }

    // Construct the custom element.
    constructor() {
        super();

        // Set default values.
        if (!this.hasAttribute('filename')) {
            this.setAttribute('filename', 'default_filename');
        }

        // Create shadow root and define element structure.
        this.attachShadow({ mode: 'open' });
        this.shadowRoot.innerHTML = `
            <link rel="stylesheet" href="/static/css/file.css">
            <div class="file">
                <div class="file-info">
                    <div class="file-name">
                        <p id="filename">${this.filename}</p>
                    </div>
                </div>
                <div class="file-delete">
                    <button class="delete-button">
                        <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M21.5 6C21.5 6.51284 21.114 6.93551 20.6166 6.99327L20.5 7H19.6553L18.4239 19.5192C18.2854 20.9269 17.1016 22 15.6871 22H8.31293C6.8984 22 5.7146 20.9269 5.57614 19.5192L4.34474 7H3.5C2.94772 7 2.5 6.55228 2.5 6C2.5 5.44772 2.94772 5 3.5 5H8.5C8.5 3.067 10.067 1.5 12 1.5C13.933 1.5 15.5 3.067 15.5 5H20.5C21.0523 5 21.5 5.44772 21.5 6ZM14.25 9.25C13.8703 9.25 13.5565 9.53215 13.5068 9.89823L13.5 10V17L13.5068 17.1018C13.5565 17.4678 13.8703 17.75 14.25 17.75C14.6297 17.75 14.9435 17.4678 14.9932 17.1018L15 17V10L14.9932 9.89823C14.9435 9.53215 14.6297 9.25 14.25 9.25ZM9.75 9.25C9.3703 9.25 9.05651 9.53215 9.00685 9.89823L9 10V17L9.00685 17.1018C9.05651 17.4678 9.3703 17.75 9.75 17.75C10.1297 17.75 10.4435 17.4678 10.4932 17.1018L10.5 17V10L10.4932 9.89823C10.4435 9.53215 10.1297 9.25 9.75 9.25ZM12 3.5C11.1716 3.5 10.5 4.17157 10.5 5H13.5C13.5 4.17157 12.8284 3.5 12 3.5Z"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;
    }

    // Deletes element when clicked.
    connectedCallback() {
        this.shadowRoot
            .querySelector('.delete-button')
            .addEventListener(
                'click', 
                () => this.deleteFile()
            );
    }

    // Removes event listener when element is deleted.
    disconnectedCallback() {
        this.shadowRoot
            .querySelector('.delete-button')
            .removeEventListener(
                'click', 
                () => this.deleteFile()
            );
    }

    // Updates element when an attribute changes.
    attributeChangedCallback(name, oldValue, newValue) {
        if (oldValue !== newValue) {
            this[name] = newValue;
        }
    }

    // Getters and setters for filename attribute.
    set filename(name) {
        this.shadowRoot
            .getElementById('filename')
            .textContent = name;
    }

    get filename() {
        return this
            .getAttribute('filename');
    }

    // Dispatches delete event and removes element.
    deleteFile() {
        this.dispatchEvent(
            new CustomEvent('delete', {
            detail: {
                filename: this.filename
            }
            })
        );
        this.remove();

        const response = fetch('/del-file', {
            method: 'POST', 
            body: JSON.stringify({
                filename: this.filename,
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
}

// Define the custom element.
customElements.define('file-item', File);

// Fetches the list of names of added files.
export async function addFile() {
    const response = await fetch('/add-file', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
    });
    // TODO: Add notification of file added.
}

document.getElementById('add-file').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function(event) {
    const files = event.target.files;
    const formData = new FormData();
    const fileList = document.getElementById('file-list');

    for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
        formData.append('filename', files[i].name);

        const file = new File();
        file.setAttribute('filename', files[i].name);
        fileList.appendChild(file);
    }

    sendFilesToBackend(formData);
});

async function sendFilesToBackend(formData) {
    fetch('/add-file', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

export async function loadFiles() {
    const response = await fetch('/load-files', {
        method: 'POST',
    });
    const data = await response.json();
    const files = data.files;
    const fileList = document.getElementById('file-list');

    for (let i = 0; i < files.length; i++) {
        const file = new File();
        file.setAttribute('filename', files[i]);
        fileList.appendChild(file);
    }
}