import torch

from transformers import AutoTokenizer, AutoModelForCausalLM

# Set up AI model and gpu acceleration config.
model_name = "meta-llama/Llama-3.2-1B"
cache_dir = "./models/Llama-3.2-1B"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {device}")
print(f"Loading model: {model_name}")

# Load the AI model and tokenizer.
tokenizer = AutoTokenizer.from_pretrained(
    model_name, 
    cache_dir=cache_dir
)
model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    cache_dir=cache_dir
)
model.to(device)

# Query the AI model and return its response.
def query(message):
    '''
    Queries the AI model with the user's message 
    and returns the response.

    Args:
        message (str): The user query for the AI model.
    Returns:
        str: The AI-generated response.
    '''

    # Ensure the padding token is set.
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Encode the message and send it to the AI.
    input_ids = tokenizer.encode(
        message, 
        return_tensors="pt"
    ).to(device)
    attention_mask = input_ids.ne(
        tokenizer.pad_token_id
    ).to(device)

    # Generate and decode the AI response.
    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=500,
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id,
        do_sample=True,
        top_p=0.9,
        no_repeat_ngram_size=2,
    )
    response = tokenizer.decode(
        output[0], 
        skip_special_tokens=True
    )

    # Remove user message from the start if present.
    if response.startswith(message):
        response = response[len(message) + 1:].strip()

    return response