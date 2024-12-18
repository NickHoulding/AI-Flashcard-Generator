from flask import Flask, render_template, request, jsonify
from PyQt5.QtWidgets import QApplication, QFileDialog
from query import query

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
    file_path, _ = file_dialog.getOpenFileName(
        caption='Select a file',
        filter='Text files (*.txt);;PDF files (*.pdf)'
    )

    if file_path:
        file_name = file_path.split('/')[-1]
    else:
        file_name = None

    return jsonify({'filename': file_name})

if __name__ == '__main__':
    app.run(host='127.0.0.1')