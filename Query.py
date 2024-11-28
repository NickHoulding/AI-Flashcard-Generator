import os  
from openai import AzureOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM


# Storage structure: {display_name: (deployment_name, endpoint_url)}
models = {
    "Llama-3.2-1B-Instruct": None, # Local model
}


API_KEY = ""


def get_models():
    return list(models.keys())


def send_query(text, model):
    if models[model] is not None:
        return cloud_query(text, model)
    else:
        return local_query(text, model)


def cloud_query(text, model_name):
    endpoint = os.getenv("ENDPOINT_URL", models[model_name][1])
    deployment = os.getenv("DEPLOYMENT_NAME", models[model_name][0])
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", API_KEY)

    client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version="2024-05-01-preview",  
    )  

    chat_prompt = [
        {
            "role": "system",
            "content": "You are the best AI assistant helping students create Quizlet flashcards to study. You strictly create these flashcards in the format: \"Question;Answer\". do not number the questions."
        },
        {
            "role": "user",
            "content": "Here is my text to convert into flashcards: " + text
        }
    ]

    speech_result = chat_prompt  

    completion = client.chat.completions.create(  
        model=deployment,  
        messages=speech_result,  
        max_tokens=800,  
        temperature=0.0,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False  
    )  
    
    return completion.choices[0].message.content


from transformers import AutoTokenizer, AutoModelForCausalLM

def local_query(text, model_name):
    model_name = "./meta-llama-3.2-1B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    if tokenizer.eos_token is None:
        tokenizer.add_special_tokens({'eos_token': '</s>'})
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model.config.pad_token_id = tokenizer.pad_token_id

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=100,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response