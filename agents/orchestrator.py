from agents.industry_agent import industry_research
from agents.competitor_agent import competitor_analysis
from agents.trend_agent import trend_analysis
from agents.report_writer import generate_report
from agents.web_research_agent import web_research


def run_market_research(topic):

    print("Searching the web...")
    sources = web_research(topic)

    print("Running Industry Research...")
    industry = industry_research(topic)

    print("Running Competitor Analysis...")
    competitors = competitor_analysis(topic)

    print("Running Trend Analysis...")
    trends = trend_analysis(topic)

    print("Generating Final Report...")
    report = generate_report(topic, industry, competitors, trends, sources)

    return report