from flask import Flask, render_template, request, jsonify
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

if __name__ == '__main__':
    app.run(host='127.0.0.1')