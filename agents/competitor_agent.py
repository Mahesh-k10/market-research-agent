from config import client, MODEL

def competitor_analysis(topic):

    prompt = f"""
    Identify and analyze major companies in the {topic} market.

    Provide:

    - Top companies
    - Products/services
    - Market strategy
    - Competitive advantage

    Present the result as structured analysis.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content