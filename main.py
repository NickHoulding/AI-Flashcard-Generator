from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, render_template, request, jsonify
import torch

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "meta-llama/Llama-3.2-1B-Instruct"
cache_dir = "./models/Llama-3.2-1B-instruct"

print(f"Using device: {device}")
print(f"Loading model: {model_name}")

tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)
model.to(device)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')
    response = query(message)
    return jsonify({'response': response})

def query(message):
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    input_ids = tokenizer.encode(message, return_tensors="pt").to(device)

    attention_mask = input_ids.ne(tokenizer.pad_token_id).to(device)

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=1000,
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id,
        do_sample=True,
        no_repeat_ngram_size=2,
    )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1')