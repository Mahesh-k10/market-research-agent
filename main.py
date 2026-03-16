from agents.orchestrator import run_market_research

def main():

    topic = input("Enter research topic: ")

    report = run_market_research(topic)

    with open("market_research_report.txt", "w") as f:
        f.write(report)

    print("\nResearch completed. Report saved.")


if __name__ == "__main__":
    main()