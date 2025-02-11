import requests
import ollama
import shutil
import os
import io
from flask import Flask, render_template, request, jsonify
from PyQt5.QtWidgets import QApplication, QFileDialog
from rag import update_database, del_from_chroma, get_file_names
from flaskwebgui import FlaskUI
from query import query

app = Flask(__name__)

@app.route('/')
def main():
    """
    Renders the Flask application.

    Args:
        None
    Returns:
        Rendered HTML template.
    """
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message() -> tuple[jsonify, int]:
    """
    Sends user messages to the AI.

    Args:
        None
    Returns:
        tuple[jsonify, int]: AI response and HTTP code.
    """
    data = request.get_json()
    message = data.get('message', '')
    ret_msg = None

    if not message:
        ret_msg = jsonify({
            'error': 'Message is required'
        }), 400
        return ret_msg

    response, sources = query(message)

    ret_msg = jsonify({
        'message': {
            'content': response,
            'sources': sources
        }
    }), 200

    return ret_msg

@app.route('/add-file', methods=['POST'])
def add_file() -> tuple[jsonify, int]:
    """
    Ingests uploaded pdfs and updates the database.

    Args:
        None
    Returns:
        tuple[jsonify, int]: JSON response and HTTP code.
    """
    uploaded_files = request.files.getlist('file')
    filenames = request.form.getlist('filename')
    ret_msg = None

    for file, filename in zip(uploaded_files, filenames):
        file.save(os.path.join('./tmp', filename))

    update_database()

    for filename in filenames:
        os.remove(os.path.join('./tmp', filename))
    
    ret_msg = jsonify({
        'message': 'File(s) addition finished'
    }), 200

    return ret_msg

@app.route('/del-file', methods=['POST'])
def deleteFile() -> tuple[jsonify, int]:
    """
    Deletes all data from a file in the database.

    Args:
        None
    Returns:
        tuple[jsonify, int]: JSON response and HTTP code.
    """
    data = request.get_json()
    filename = data.get('filename', '')
    ret_msg = None

    if not filename:
        ret_msg = jsonify({
            'error': 'Filename is required'
        }), 400
        return ret_msg

    del_from_chroma(filename)

    ret_msg = jsonify({
        'message': 'File deletion finished'
    }), 200

    return ret_msg

@app.route('/load-files', methods=['POST'])
def loadFiles() -> tuple[jsonify, int]:
    """
    Loads the files present in the database.

    Args:
        None
    Returns:
        tuple[jsonify, int]: JSON response and HTTP code.
    """
    
    return jsonify({
        'files': get_file_names()
    })

if __name__ == '__main__':
    ui = FlaskUI(
        app=app, 
        server='flask'
    )
    ui.run()