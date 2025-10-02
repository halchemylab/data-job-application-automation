from openai import OpenAI, APIError, RateLimitError, AuthenticationError
import os
import json
from dotenv import load_dotenv
from src.logger import logger

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OpenAI API key not found. Make sure to set it in a .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def extract_job_details_from_text(text):
    """Sends text to OpenAI for structured extraction."""
    prompt = f"""
    Extract structured information from the following job posting and return it as a JSON object.

    {text}

    ### **JSON Schema**
    {{
      "Job Position": "string",
      "Company Name": "string",
      "Specific Job Project": "string",
      "Required IT Skills": "string (comma-separated)",
      "Job Type": "string (e.g., Full-Time, Part-Time, Contract)",
      "Remote Work": "string (Yes/No)",
      "Job Description Summary": "string (1-2 sentences)",
      "Perks Summary": "string (1-2 sentences)"
    }}

    If a value is not found, use "Unknown".
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an expert in extracting job details and returning them as a valid JSON object."},
                {"role": "user", "content": prompt}
            ]
        )
    except AuthenticationError as e:
        logger.error(f"OpenAI authentication error: {e}")
        return None
    except RateLimitError as e:
        logger.error(f"OpenAI rate limit exceeded: {e}")
        return None
    except APIError as e:
        logger.error(f"Error with OpenAI API: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred with the OpenAI API: {e}")
        return None

    try:
        extracted_data = response.choices[0].message.content
        job_details_dict = json.loads(extracted_data)
    except (json.JSONDecodeError, IndexError) as e:
        logger.error(f"Failed to parse JSON response from OpenAI: {e}")
        logger.debug(f"Invalid JSON response: {extracted_data}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while parsing the OpenAI response: {e}")
        return None

    return job_details_dict