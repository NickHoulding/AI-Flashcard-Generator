import os  
from openai import AzureOpenAI

# Storage structure: {display_name: (deployment_name, endpoint_url)}
models = {

}

API_KEY = ""
# Above information has been removed in the pushed code for security reasons

# Get the list of available models
def get_models():
    return list(models.keys())

# Send a query to the Azure OpenAI API
def send_query(text, model):
    endpoint = os.getenv("ENDPOINT_URL", models[model][1])
    deployment = os.getenv("DEPLOYMENT_NAME", models[model][0])
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", API_KEY)

    # Initialize Azure OpenAI client with key-based authentication
    client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version="2024-05-01-preview",  
    )  

    # Prepare the chat prompt
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

    # Include speech result if speech is enabled  
    speech_result = chat_prompt  

    # Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,  
        messages=speech_result,  
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False  
    )  
    
    return completion.choices[0].message.content