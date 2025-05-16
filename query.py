import os
from rag import get_context_prompt
from config import get_env_var
from pydantic import BaseModel
from ollama import chat

class Flashcard(BaseModel):
    question: str
    answer: str

    def to_dict(self):
        """
        Converts the flashcard to a dictionary.

        Args:
            None

        Returns:
            dict: The flashcard as a dictionary.

        Raises:
            None
        """
        return {
            "question": self.question,
            "answer": self.answer,
        }

class StudySet(BaseModel):
    flashcards: list[Flashcard]

def query_ollama(
        prompt: str
    ) -> str:
    """
    Queries the Ollama model with the user's prompt.

    Args:
        prompt (str): The prompt to query the model.
    
    Returns:
        html_response (str): Ollama AI response.
    
    Raises:
        None
    """
    response = chat(
        messages=[{
                "role": "user",
                "content": f"""
                    Create a list of flashcards based on the prompt: {prompt}"""
            }],
        model=get_env_var("MODEL"),
        format=StudySet.model_json_schema()
    )

    study_set = StudySet.model_validate_json(response.message.content)
    flashcards = [card.to_dict() for card in study_set.flashcards]

    return flashcards

def get_sources(
        results: list
    ) -> list[str]:
    """
    Retrieves the sources from the database results.

    Args:
        results (list): The results from the database.
    
    Returns:
        list[str]: The sources of the documents.
    
    Raises:
        None
    """
    sources = set()
    for doc in results:
        source = doc.metadata.get("source")

        if source not in sources:
            sources.add(os.path.basename(source))

    return list(sources)

def query(
        query_text: str
    ) -> tuple[str, str]:
    """
    Handles database retrieval and AI queries.

    Args:
        query_text (str): Database query text.
    
    Returns:
        tuple[str, str]: AI flashcards and sources.
    
    Raises:
        None
    """
    prompt, results = get_context_prompt(query_text)
    flashcards = query_ollama(prompt)
    sources = get_sources(results)

    return flashcards, sources