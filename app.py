import threading
from rag import del_from_chroma, get_file_names, process_file
from flask import Flask, render_template, request, jsonify
from flaskwebgui import FlaskUI
from query import query
from typing import Text

db_operation_lock = threading.Lock()
app = Flask(__name__)

@app.route('/')
def main(
    ) -> Text:
    """
    Renders the Flask application.

    Args:
        None
    
    Returns:
        Rendered HTML template.
    
    Raises:
        None
    """
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message(
    ) -> jsonify:
    """
    Sends user messages to the AI.

    Args:
        None
    
    Returns:
        jsonify: AI response with HTTP code.
    
    Raises:
        None
    """
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({
            'error': 'Message is required',
            'status': 400
        })

    response, sources = query(message)

    return jsonify({
        'message': {
            'content': response,
            'sources': sources
        },
        'status': 200
    })

@app.route('/add-file', methods=['POST'])
def add_file(
    ) -> jsonify:
    """
    Ingests uploaded pdfs and processes each individually in memory.

    Args:
        None
    
    Returns:
        jsonify: JSON response with HTTP code.
    
    Raises:
        None
    """
    uploaded_file = request.files.get('file')
    filename = request.form.get('filename')
    
    if not uploaded_file or not filename:
        return jsonify({
            'error': 'File and filename are required',
            'status': 400
        })

    with db_operation_lock:
        file_content = uploaded_file.read()
        process_file(file_content, filename)
    
    return jsonify({
        'message': 'File added successfully',
        'status': 200
    })

@app.route('/del-file', methods=['POST'])
def deleteFile(
    ) -> jsonify:
    """
    Deletes all data from a file in the database.

    Args:
        None
    
    Returns:
        jsonify: JSON response and HTTP code.
    
    Raises:
        None
    """
    data = request.get_json()
    filename = data.get('filename', '')

    if not filename:
        return jsonify({
            'error': 'Filename is required',
            'status': 400
        })

    with db_operation_lock:
        del_from_chroma(filename)

    return jsonify({
        'message': 'File deletion finished',
        'status': 200
    })

@app.route('/load-files', methods=['POST'])
def loadFiles(
    ) -> jsonify:
    """
    Loads the files present in the database.

    Args:
        None
    
    Returns:
        jsonify: JSON response and HTTP code.
    
    Raises:
        None
    """
    return jsonify({
        'files': get_file_names(),
        'status': 200
    })

# Entry Point
if __name__ == '__main__':
    ui = FlaskUI(
        app=app, 
        server='flask'
    )
    ui.run()