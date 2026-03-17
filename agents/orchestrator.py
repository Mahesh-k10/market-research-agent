from config import client, MODEL
import time
from openai import RateLimitError

def run_market_research(topic):

    prompt = f"""
    Conduct a comprehensive market research report on: {topic}

    Include the following sections:

    1. Executive Summary
    2. Industry Overview
    3. Market Drivers
    4. Key Segments
    5. Competitive Landscape
    6. Key Technologies
    7. Market Trends
    8. Regulatory Environment
    9. Opportunities & Risks

    Keep it structured, clear, and professional.
    """

    retries = 3

    for attempt in range(retries):
        try:
            time.sleep(2)

            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )

            return response.choices[0].message.content

        except RateLimitError:
            if attempt < retries - 1:
                time.sleep(5)
            else:
                return "⚠️ API limit reached. Please try again later."

        except Exception as e:
            return f"❌ Error: {str(e)}"
