from config import client, MODEL


def generate_report(topic, industry, competitors, trends, sources):

    source_text = "\n".join(
        [f"{s['title']} - {s['link']}" for s in sources]
    )

    prompt = f"""
Create a professional market research report.

Topic: {topic}

Industry Analysis:
{industry}

Competitor Analysis:
{competitors}

Market Trends:
{trends}

Web Sources:
{source_text}

Structure the report:

1. Executive Summary
2. Industry Overview
3. Market Landscape
4. Competitive Analysis
5. Emerging Trends
6. Strategic Insights
7. Future Outlook
8. References (use the sources provided)

Write a detailed consulting-style report.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content