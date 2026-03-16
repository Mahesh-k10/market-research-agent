from tools.web_search import search_web

def web_research(topic):

    queries = [
        f"{topic} market size",
        f"{topic} industry trends",
        f"{topic} major companies",
        f"{topic} growth forecast"
    ]

    all_results = []

    for q in queries:
        results = search_web(q, 3)
        all_results.extend(results)

    return all_results