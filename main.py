import requests
import ollama
import shutil
import os
import io

from flask import Flask, render_template, request, jsonify
from PyQt5.QtWidgets import QApplication, QFileDialog
from populate_database import update_database
from query_data import query_rag, delete_file_chunks
from flaskwebgui import FlaskUI

app = Flask(__name__)

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

    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({
            'error': 'Message is required'
        }), 400

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
    Processes incoming files, saves them to the local directory,
    """

    uploaded_files = request.files.getlist('file')
    filenames = request.form.getlist('filename')

    for file, filename in zip(uploaded_files, filenames):
        if file:
            file.save(os.path.join('./tmp', filename))

    update_database()

    for filename in filenames:
        try:
            os.remove(os.path.join('./tmp', filename))
        except:
            pass

    return jsonify({
        'message': 'Files received'
    })

# Handle user requests to delete a file.
@app.route('/del-file', methods=['POST'])
def deleteFile():
    """
    Deletes all chunks in the database associated with the specified file.

    Args:
        None
    Returns:
        None
    """
    filename = request.get_json().get('filename')
    delete_file_chunks(filename)
    # Return json confirming deletion.
    return

if __name__ == '__main__':
    ui = FlaskUI(
        app=app, 
        server='flask'
    )
    ui.run()