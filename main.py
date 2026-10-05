"""
Main CLI entry point for Sales & CRM Research Agent.
Demonstrates end-to-end execution of the LangGraph agent calling MCP tools and RAG knowledge.
"""

import sys
import json
from agent.graph import run_sales_agent

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    print("=" * 80)
    print("  Enterprise Sales / CRM Research Agent (FDE Project Demonstration)  ")
    print("=" * 80)

    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Give me a summary of customer ABC and tell me what I should discuss in tomorrow's meeting."
    )

    print(f"\n[USER QUERY]: \"{query}\"\n")
    print(">>> Triggering LangGraph Workflow:")
    print("    [1. Intent Analysis] -> [2. MCP Server Tools] -> [3. RAG Engine] -> [4. Synthesizer] -> [5. Guardrails]\n")

    result = run_sales_agent(query)

    print("-" * 80)
    print(result["final_briefing"])
    print("-" * 80)

    print("\n[GUARDRAIL AUDIT CHECK]:")
    for check in result["risk_assessment"]:
        print(f"  * {check}")

    print("\n[RAG KNOWLEDGE SOURCES RETRIEVED]:")
    for src in result.get("rag_context", {}).get("sources", []):
        print(f"  * {src}")

    print("\n[WORKFLOW AUDIT TRACE]:")
    for step in result.get("audit_trace", []):
        node_name = step.get("node")
        details = {k: v for k, v in step.items() if k not in ["node", "timestamp"]}
        print(f"  * {node_name}: {json.dumps(details)}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
