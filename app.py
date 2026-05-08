import os
import streamlit as st

from graph import graph


st.set_page_config(
    page_title="Agentic Security AI",
    layout="wide"
)

st.title(
    "🛡️ Agentic AI Security Investigator"
)

st.sidebar.header("Configuration")

st.sidebar.write(
    f"Model: {os.getenv('GROQ_MODEL')}"
)

st.markdown(
    """
This system performs:

- AI-powered crawling
- Threat extraction
- Threat intelligence lookup
- Security report generation
"""
)

url = st.text_input(
    "Enter URL",
    placeholder="https://attack.mitre.org/"
)

run_button = st.button(
    "Run Investigation"
)

if run_button and url:

    # URL validation
    if not url.startswith("http"):

        st.error(
            "Please enter a valid URL starting with http or https"
        )

        st.stop()

    st.divider()

    # Create tabs
    tab1, tab2 = st.tabs([
        "⚡ Execution Logs",
        "📄 Final Report"
    ])

    # LOGS TAB
    with tab1:

        st.subheader("Live Workflow Execution")

        log_container = st.empty()

        logs = []

        def ui_logger(message):

            logs.append(message)

            formatted = "\n".join(logs)

            log_container.markdown(
                f"""
```bash
{formatted}
```
"""
            )

    # RUN WORKFLOW
    with st.spinner(
        "Running agentic workflow..."
    ):

        result = graph.invoke({

            "url": url,

            "logger": ui_logger
        })

    # REPORT TAB
    with tab2:

        st.subheader("Generated Security Report")

        # Render markdown beautifully
        st.markdown(
            result["final_report"]
        )

        # OPTIONAL THREAT DISPLAY
        if result.get("threats"):

            st.subheader("Detected Threats")

            for threat in result["threats"][:10]:

                severity = threat.get(
                    "severity",
                    "Unknown"
                )

                if severity == "Critical":
                    icon = "🚨"

                elif severity == "High":
                    icon = "⚠️"

                else:
                    icon = "ℹ️"

                with st.expander(
                    f"{icon} "
                    f"{threat['threat']} "
                    f"({severity})"
                ):

                    st.write(
                        f"**Category:** "
                        f"{threat['category']}"
                    )

                    st.write(
                        f"**Description:**"
                    )

                    st.write(
                        threat["description"]
                    )

                    st.write(
                        "**Indicators:**"
                    )

                    indicators = threat.get(
                        "matched_indicators",
                        []
                    )

                    if indicators:

                        for indicator in indicators:

                            st.write(
                                f"- {indicator}"
                            )

                    st.write(
                        "**Recommended Fixes:**"
                    )

                    fixes = threat.get(
                        "fix",
                        []
                    )

                    if isinstance(fixes, list):

                        for fix in fixes:

                            st.write(
                                f"- {fix}"
                            )

                    else:

                        st.write(fixes)

        else:

            st.success(
                "No significant threats detected."
            )
