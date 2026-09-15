import os

import cohere
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("COHERE_API_KEY")


def generate_response(messages):
    """
    Send conversation messages to Cohere
    and return the generated response text.
    """

    if not API_KEY:
        raise ValueError(
            "COHERE_API_KEY is missing. Check your .env file."
        )

    try:
        client = cohere.ClientV2(api_key=API_KEY)

        response = client.chat(
            model="command-a-03-2025",
            messages=messages
        )

        if not response.message.content:
            raise RuntimeError("The AI returned an empty response.")

        return response.message.content[0].text

    except Exception as e:
        raise RuntimeError(f"AI API request failed: {e}")