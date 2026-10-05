"""
LangGraph State Schema for the Sales & CRM Research Agent.
Tracks conversational inputs, MCP tool results, RAG context, and executive briefings.
"""

from typing import TypedDict, List, Dict, Any, Optional


class SalesAgentState(TypedDict):
    # User Input & Intent
    user_query: str
    target_customer_name: Optional[str]
    intent: str  # e.g., 'meeting_prep', 'account_overview', 'deal_inquiry'

    # MCP CRM Retrieved Entities
    customer_profile: Optional[Dict[str, Any]]
    deals: List[Dict[str, Any]]
    previous_interactions: List[Dict[str, Any]]
    support_tickets: List[Dict[str, Any]]
    mcp_error: Optional[str]

    # Computed Highlights
    current_deal_summary: Optional[Dict[str, Any]]
    last_interaction_date: Optional[str]
    last_interaction_summary: Optional[str]
    open_tickets_count: int
    open_tickets_list: List[Dict[str, Any]]
    interested_product: Optional[str]

    # RAG Knowledge Context
    rag_context: Dict[str, Any]  # product_docs, pricing_docs, case_studies, playbooks, sources

    # Generated Strategy & Executive Briefing
    recommended_discussion_agenda: List[str]
    risk_assessment: List[str]
    final_briefing: str

    # Workflow Metadata & Audit Trail
    audit_trace: List[Dict[str, Any]]
    current_step: str
