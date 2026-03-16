from config import client, MODEL

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

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content