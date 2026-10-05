"""
Automated Pytest Suite for Sales & CRM Research Agent.
Verifies MCP tools, RAG retriever, and LangGraph workflow nodes.
"""

import pytest
from mcp_server.server import get_customer, get_deals, get_previous_interactions, get_support_tickets
from rag_engine.retriever import kb_retriever
from agent.graph import run_sales_agent


def test_mcp_get_customer():
    res = get_customer("ABC Corp")
    assert res["status"] == "success"
    data = res["data"]
    assert data["name"] == "ABC Corp"
    assert data["id"] == "CUST-001"
    assert "Rajesh Sharma" in data["primary_contact"]["name"]


def test_mcp_get_deals():
    res = get_deals("CUST-001")
    assert res["status"] == "success"
    assert res["count"] >= 1
    deal = res["deals"][0]
    assert "25L" in deal["value_inr"] or "25,00,000" in deal["value_inr"]
    assert deal["interested_product"] == "Enterprise AI"


def test_mcp_get_support_tickets():
    res = get_support_tickets("CUST-001", status="OPEN")
    assert res["status"] == "success"
    assert res["open_count"] == 2
    ticket_ids = [t["id"] for t in res["tickets"]]
    assert "TICK-9021" in ticket_ids
    assert "TICK-9034" in ticket_ids


def test_rag_retrieval():
    ctx = kb_retriever.retrieve_context_for_deal("Enterprise AI", "Banking", True)
    assert len(ctx["sources"]) >= 4
    # Check that Case Study X is present
    has_case_x = any("Case Study X" in s for s in ctx["sources"])
    assert has_case_x


def test_end_to_end_sales_agent():
    query = "Give me a summary of customer ABC and tell me what I should discuss in tomorrow's meeting."
    result = run_sales_agent(query)
    briefing = result["final_briefing"]

    # Check key FDE metrics in output
    assert "ABC Corp" in briefing
    assert "25L" in briefing or "25,00,000" in briefing
    assert "Open support issues" in briefing and "2" in briefing
    assert "Enterprise AI" in briefing
    assert "Case Study X" in briefing

    # Check compliance guardrail
    risks = result["risk_assessment"]
    assert any("VERIFIED" in r for r in risks)
    assert any("Agenda Item #1" in r for r in risks)
