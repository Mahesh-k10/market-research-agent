from config import client, MODEL

def trend_analysis(topic):

    prompt = f"""
    Analyze emerging trends in the {topic} market.

    Include:

    - Technology trends
    - Investment trends
    - Startup ecosystem
    - Future predictions (5–10 years)

    Provide insights like a consulting report.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content