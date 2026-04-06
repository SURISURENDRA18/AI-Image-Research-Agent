import base64
import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, OpenAIError

# Load environment variables
load_dotenv()


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    return OpenAI(api_key=api_key)


def analyze_image(image_bytes):
    try:
        client = get_client()

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this image. Extract objects, patterns, and insights."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ],
                }
            ],
            max_tokens=500
        )

        # Safety check
        if not response.choices or not response.choices[0].message.content:
            return {
                "error": "Empty response from AI model"
            }

        text = response.choices[0].message.content

        return {
            "description": text,
            "objects": extract_keywords(text)
        }

    except RateLimitError:
        return {
            "error": "API quota exceeded. Please check billing."
        }

    except OpenAIError as e:
        return {
            "error": f"OpenAI error: {str(e)}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }


def extract_keywords(text):
    # safer keyword extraction
    words = text.split()
    unique_words = list(set(words))
    return unique_words[:10]
