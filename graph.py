from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from crawler import run_crawler

from agents import (
    analysis_agent,
    extract_threats_agent,
    report_agent
)

from tools import search_threats


class AgentState(TypedDict):

    url: str

    crawled_content: str

    analysis: str

    extracted_threats: str

    threats: list

    final_report: str

    logger: object


def log_message(state, msg):

    logger = state.get("logger")

    if logger:
        logger(msg)

    print(msg)


def crawl_node(state: AgentState):

    log_message(
        state,
        "\n===== NODE 1: CRAWLER AGENT ====="
    )

    content = run_crawler(
        state["url"],
        logger=state.get("logger")
    )

    return {
        "crawled_content": content
    }


def analysis_node(state: AgentState):

    log_message(
        state,
        "\n===== NODE 2: ANALYSIS AGENT ====="
    )

    log_message(
        state,
        "Analyzing security content..."
    )

    analysis = analysis_agent(
        state["crawled_content"]
    )

    log_message(
        state,
        "✓ Analysis complete"
    )

    return {
        "analysis": analysis
    }


def threat_extraction_node(
    state: AgentState
):

    log_message(
        state,
        "\n===== NODE 3: THREAT EXTRACTION AGENT ====="
    )

    extracted = extract_threats_agent(
        state["crawled_content"]
    )

    log_message(
        state,
        f"Extracted Threats:\n{extracted}"
    )

    return {
        "extracted_threats": extracted
    }


def threat_lookup_node(state: AgentState):

    log_message(
        state,
        "\n===== NODE 4: THREAT LOOKUP AGENT ====="
    )

    threats = search_threats(
        state["extracted_threats"]
    )

    if threats:

        log_message(
            state,
            f"✓ Threats Found "
            f"({len(threats)}):"
        )

        for threat in threats[:10]:

            log_message(
                state,
                f"  • {threat['threat']}"
            )

    else:

        log_message(
            state,
            "✓ No significant threats detected"
        )

    return {
        "threats": threats
    }


def report_node(state: AgentState):

    log_message(
        state,
        "\n===== NODE 5: REPORT GENERATOR ====="
    )

    report = report_agent(
        state["analysis"],
        state["threats"]
    )

    log_message(
        state,
        "✓ Final report generated"
    )

    return {
        "final_report": report
    }


workflow = StateGraph(AgentState)

workflow.add_node(
    "crawl_node",
    crawl_node
)

workflow.add_node(
    "analysis_node",
    analysis_node
)

workflow.add_node(
    "threat_extraction_node",
    threat_extraction_node
)

workflow.add_node(
    "threat_lookup_node",
    threat_lookup_node
)

workflow.add_node(
    "report_node",
    report_node
)

workflow.set_entry_point(
    "crawl_node"
)

workflow.add_edge(
    "crawl_node",
    "analysis_node"
)

workflow.add_edge(
    "analysis_node",
    "threat_extraction_node"
)

workflow.add_edge(
    "threat_extraction_node",
    "threat_lookup_node"
)

workflow.add_edge(
    "threat_lookup_node",
    "report_node"
)

workflow.add_edge(
    "report_node",
    END
)

graph = workflow.compile()