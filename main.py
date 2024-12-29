import requests
import ollama
import shutil
import os

from flask import Flask, render_template, request, jsonify
from PyQt5.QtWidgets import QApplication, QFileDialog
from populate_database import update_database
from query_data import query_rag
from flaskwebgui import FlaskUI

# Set up Flask app and AI model.
app = Flask(__name__)
ollama_url = "http://127.0.0.1:11434/api/chat"
model_name = "llama3.2"

# Renders the Flask app.
@app.route('/')
def main():
    return render_template('index.html')

# Handle user messages to the AI model.
@app.route('/send-message', methods=['POST'])
def send_message():
    """
    Processes incoming messages, queries the RAG system, 
    and returns the response along with the sources.
    
    Args:
        None
    Returns:
        Response: A JSON response containing:
            - message (dict): A dictionary with:
                - content (str): The AI-generated html response.
                - sources (str): The html formatted sources to 
                generate the response.
    """

    # Get the message from the request.
    data = request.get_json()
    message = data.get('message', '')

    # Check if the message is empty.
    if not message:
        return jsonify({
            'error': 'Message is required'
        }), 400

    # Query the RAG system and return the response.
    response, sources = query_rag(message)
    return jsonify({
        'message': {
            'content': response,
            'sources': sources
        }
    })

# Handle user requests to add file content.
@app.route('/add-file', methods=['POST'])
def add_file():
    """
    Processes user-selected files to add to the RAG
    system's knowledge base.

    Args:
        None
    Returns:
        Response: A JSON response containing:
            - filenames (list): A list of filenames 
            that were added.
    """

    # Get the file paths from the user.
    app = QApplication([])
    file_dialog = QFileDialog()
    file_paths = file_dialog.getOpenFileNames(
        caption='Select File', 
        filter='*.pdf;;*.txt'
    )

    if len(file_paths[0]) > 0:
        # Copy selected files to temp data directory.
        file_names = ([
            os.path.basename(file_path) 
            for file_path in file_paths[0]
        ])

        for file_path in file_paths[0]:
            shutil.copy(file_path, 'data')

        # Update the RAG system's knowledge base.
        update_database()

        # Clear the temp data directory.
        for file_name in file_names:
            shutil.os.remove(f"./data/{file_name}")
    else:
        file_names = None

    # Return the filenames that were added.
    return jsonify({'filenames': file_names})

# Runs the Flask app.
if __name__ == '__main__':
    ui = FlaskUI(
        app=app, 
        server='flask'
    )
    ui.run()