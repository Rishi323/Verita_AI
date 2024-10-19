import os
import logging
from openai import OpenAI, OpenAIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in the environment variables")
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def test_openai_connection():
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello, OpenAI!"}]
        )
        logger.info("OpenAI API connection test successful")
        return True
    except OpenAIError as e:
        logger.error(f"OpenAI API connection test failed: {e}")
        return False

def send_openai_request(prompt: str, model: str = "gpt-4o") -> str:
    try:
        logger.info(f"Sending request to OpenAI API with model: {model}")
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")
        logger.info("Successfully received response from OpenAI API")
        return content.strip()  # Remove any leading/trailing whitespace
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in send_openai_request: {e}")
        raise

# Test the OpenAI connection when the module is imported
if test_openai_connection():
    logger.info("OpenAI API connection is working correctly")
else:
    logger.warning("OpenAI API connection test failed. Please check your API key and network connection.")
