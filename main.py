import requests
import ollama
import shutil
import os

from flask import Flask, render_template, request, jsonify
from flaskwebgui import FlaskUI
from PyQt5.QtWidgets import QApplication, QFileDialog
from populate_database import update_database
from query_data import query_rag

app = Flask(__name__)
ollama_url = "http://127.0.0.1:11434/api/chat"
model_name = "llama3.2"

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    response = query_rag(message)

    return jsonify({
        'message': {
            'content': response,
        }
    })

@app.route('/add-file', methods=['POST'])
def add_file():
    app = QApplication([])
    file_dialog = QFileDialog()
    file_paths = file_dialog.getOpenFileNames(
        caption='Select File', 
        filter='*.pdf;;*.txt'
    )

    if len(file_paths[0]) > 0:
        file_names = [os.path.basename(file_path) for file_path in file_paths[0]]

        for file_path in file_paths[0]:
            shutil.copy(file_path, 'data')

        update_database()

        for file_name in file_names:
            shutil.os.remove(f"./data/{file_name}")
    else:
        file_names = None

    return jsonify({'filenames': file_names})

if __name__ == '__main__':
    ui = FlaskUI(app=app, server='flask')
    ui.run()