from graph import graph


def run():

    print("\n=== Agentic AI Security Investigator ===\n")

    url = input("Enter URL to investigate: ")

    result = graph.invoke({
        "url": url
    })

    print("\n===== FINAL SECURITY REPORT =====\n")

    print(result["final_report"])


if __name__ == "__main__":
    run()