"""
Sales & CRM Research Agent StateGraph Definition.
Connects intent parsing, MCP tool execution, RAG knowledge retrieval, strategy synthesis,
and compliance guardrails with conditional routing.
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from .state import SalesAgentState
from .nodes import (
    intent_analyzer_node,
    fetch_crm_data_node,
    rag_retrieval_node,
    sales_strategy_synthesizer_node,
    compliance_guardrail_node,
)


def crm_routing_condition(state: SalesAgentState) -> Literal["rag_retrieval", "__end__"]:
    """
    Evaluates whether CRM data retrieval succeeded.
    Routes to RAG if valid; terminates early if customer not found.
    """
    if state.get("mcp_error"):
        return "__end__"
    return "rag_retrieval"


def build_sales_agent_graph():
    """
    Builds and compiles the production LangGraph state machine.
    """
    workflow = StateGraph(SalesAgentState)

    # Register Nodes
    workflow.add_node("intent_analyzer", intent_analyzer_node)
    workflow.add_node("fetch_crm", fetch_crm_data_node)
    workflow.add_node("rag_retrieval", rag_retrieval_node)
    workflow.add_node("synthesizer", sales_strategy_synthesizer_node)
    workflow.add_node("compliance_guardrail", compliance_guardrail_node)

    # Define Edges & Flow
    workflow.add_edge(START, "intent_analyzer")
    workflow.add_edge("intent_analyzer", "fetch_crm")

    # Conditional Routing from CRM Fetch
    workflow.add_conditional_edges(
        "fetch_crm",
        crm_routing_condition,
        {
            "rag_retrieval": "rag_retrieval",
            "__end__": END,
        },
    )

    workflow.add_edge("rag_retrieval", "synthesizer")
    workflow.add_edge("synthesizer", "compliance_guardrail")
    workflow.add_edge("compliance_guardrail", END)

    return workflow.compile()


# Global compiled app
sales_agent_app = build_sales_agent_graph()


def run_sales_agent(user_query: str) -> SalesAgentState:
    """
    Convenience function to execute the LangGraph agent for a user query.
    """
    initial_state: SalesAgentState = {
        "user_query": user_query,
        "target_customer_name": None,
        "intent": "unknown",
        "customer_profile": None,
        "deals": [],
        "previous_interactions": [],
        "support_tickets": [],
        "mcp_error": None,
        "current_deal_summary": None,
        "last_interaction_date": None,
        "last_interaction_summary": None,
        "open_tickets_count": 0,
        "open_tickets_list": [],
        "interested_product": None,
        "rag_context": {},
        "recommended_discussion_agenda": [],
        "risk_assessment": [],
        "final_briefing": "",
        "audit_trace": [],
        "current_step": "initialized",
    }

    result = sales_agent_app.invoke(initial_state)
    return result
