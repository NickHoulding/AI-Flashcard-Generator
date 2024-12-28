import torch

from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "meta-llama/Llama-3.2-1B"
cache_dir = "./models/Llama-3.2-1B"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")
print(f"Loading model: {model_name}")

tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)
model.to(device)

def query(message):
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    input_ids = tokenizer.encode(message, return_tensors="pt").to(device)
    attention_mask = input_ids.ne(tokenizer.pad_token_id).to(device)

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=500,
        temperature=0.01,
        pad_token_id=tokenizer.pad_token_id,
        do_sample=True,
        top_p=0.9,
        no_repeat_ngram_size=2,
    )

    response = tokenizer.decode(output[0], skip_special_tokens=True)

    if response.startswith(message):
        response = response[len(message) + 1:].strip()

    return response