import os
import time
import logging

from dotenv import load_dotenv
from google import genai

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def ask_gemini(
    prompt,
    model="gemini-3.6-flash",
    retries=3,
    initial_delay=2
):
    """
    Calls Gemini with retry and exponential backoff.
    """

    delay = initial_delay

    for attempt in range(1, retries + 1):

        try:

            logging.info(
                f"Calling Gemini (Attempt {attempt}/{retries})"
            )

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            logging.info("Gemini Success")

            return response.text

        except Exception as e:

            logging.warning(
                f"Attempt {attempt} failed: {e}"
            )

            if attempt == retries:

                logging.error(
                    "All Gemini attempts failed."
                )

                raise

            logging.info(
                f"Retrying in {delay} seconds..."
            )

            time.sleep(delay)

            delay *= 2