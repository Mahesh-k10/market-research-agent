from config import client, MODEL
import time
from openai import RateLimitError

def industry_research(topic):

    prompt = f"""
    Conduct detailed industry research about: {topic}

    Include:

    1. Industry Overview
    2. Market Drivers
    3. Key Segments
    4. Major Technologies
    5. Regulatory Environment

    Write in professional research format.
    """

    retries = 3  # number of retry attempts

    for attempt in range(retries):
        try:
            time.sleep(2)  # prevent rate limit

            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.choices[0].message.content

        except RateLimitError:
            if attempt < retries - 1:
                time.sleep(5)  # wait before retry
            else:
                return "⚠️ Too many requests. Please try again after a minute."

        except Exception as e:
            return f"❌ Error occurred: {str(e)}"
