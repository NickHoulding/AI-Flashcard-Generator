from flask import Flask, render_template, request, jsonify
from PyQt5.QtWidgets import QApplication, QFileDialog
from query import query
import os

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')
    response = query(message)
    return jsonify({'response': response})

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
    else:
        file_names = None

    return jsonify({'filenames': file_names})

if __name__ == '__main__':
    app.run(host='127.0.0.1')