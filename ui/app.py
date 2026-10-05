"""
Streamlit Web Application for Sales / CRM Research Agent.
Provides an interactive cockpit for Sales Executives & Forward Deployed Engineers (FDEs).
"""

import sys
from pathlib import Path
import json
import streamlit as st

# Add project root to sys.path
root_path = Path(__file__).parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from agent.graph import run_sales_agent
from mcp_server.server import get_customer, get_deals, get_previous_interactions, get_support_tickets
from rag_engine.retriever import kb_retriever

st.set_page_config(
    page_title="Sales / CRM Research Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("💼 Enterprise Sales / CRM Research Agent")
st.caption("A Forward Deployed Engineer (FDE) Agentic System powered by LangGraph, MCP, and Multi-Domain RAG")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration & Controls")
    customer_choice = st.selectbox(
        "Select Enterprise Account:",
        ["ABC Corp", "Zenith Cloud Solutions"],
        index=0,
    )
    
    transport_mode = st.radio(
        "MCP Transportation Layer:",
        ["stdio (Standard Local Process)", "SSE (Server-Sent Events / HTTP)", "Direct In-Process"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 🔌 Registered MCP Tools")
    st.code("""- get_customer()
- get_deals()
- get_previous_interactions()
- get_support_tickets()""", language="text")

    st.markdown("### 📚 RAG Knowledge Collections")
    st.markdown("""
    * **Products**: Enterprise AI, Latency SLAs
    * **Pricing**: ₹25L Core Tier, Multi-Year
    * **Case Studies**: Case Study X (Tier-1 Bank)
    * **Playbooks**: CTO Meeting Alignment
    """)

# Default Query
default_query = f"Give me a summary of customer {customer_choice.split()[0]} and tell me what I should discuss in tomorrow's meeting."

st.markdown("### 💬 Natural Language Sales Request")
user_prompt = st.text_input(
    "Enter salesperson request:",
    value=default_query,
    help="Ask for account briefings, deal status, risk factors, or meeting discussion points."
)

col_run, col_clear = st.columns([1, 5])
run_clicked = col_run.button("🚀 Run Sales Agent", type="primary", use_container_width=True)

if run_clicked or "last_result" in st.session_state:
    if run_clicked:
        with st.spinner("Executing LangGraph Workflow (Intent -> MCP Tools -> RAG -> Synthesizer -> Guardrails)..."):
            result = run_sales_agent(user_prompt)
            st.session_state["last_result"] = result
    else:
        result = st.session_state["last_result"]

    st.markdown("---")

    # Top KPI Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    cust_data = result.get("customer_profile") or {}
    deal_data = result.get("current_deal_summary") or {}
    
    m1.metric("🏢 Customer", cust_data.get("name", "N/A"), cust_data.get("tier", "Enterprise"))
    m2.metric("💰 Current Deal", deal_data.get("value_inr", "₹25L"), deal_data.get("stage", "Negotiation"))
    m3.metric("📅 Last Interaction", result.get("last_interaction_date", "N/A"), "Executive Sync")
    m4.metric("⚠️ Open Support Issues", f"{result.get('open_tickets_count', 0)} Open", delta="Action Required", delta_color="inverse")

    # Tabs
    tab_brief, tab_mcp, tab_rag, tab_langgraph = st.tabs([
        "📋 Executive Briefing",
        "🔌 MCP Live CRM Data",
        "📚 RAG Knowledge Retrieved",
        "🕸️ LangGraph Architecture & Trace",
    ])

    with tab_brief:
        st.markdown(result.get("final_briefing", "No briefing generated."))
        
        st.markdown("#### 🛡️ Compliance & Guardrails Verification")
        for risk in result.get("risk_assessment", []):
            st.success(risk)

    with tab_mcp:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.subheader("👤 Customer Profile")
            st.json(result.get("customer_profile"))

            st.subheader("💼 Active Deals")
            st.json(result.get("deals"))

        with col_c2:
            st.subheader("🎟️ Support Tickets")
            tickets = result.get("support_tickets", [])
            for t in tickets:
                status_color = "red" if t.get("status") == "OPEN" else "green"
                st.markdown(f"**[{t.get('id')}]** `{t.get('status')}` - **{t.get('subject')}**")
                st.caption(f"Priority: {t.get('priority')} | Assigned: {t.get('assigned_to')} | Impact: {t.get('impact')}")

            st.subheader("📅 Interaction History")
            st.json(result.get("previous_interactions"))

    with tab_rag:
        st.subheader("Retrieved Knowledge Chunks")
        rag_data = result.get("rag_context", {})
        
        with st.expander("📄 Product Documentation Chunks", expanded=True):
            for doc in rag_data.get("product_docs", []):
                st.markdown(doc)

        with st.expander("💰 Pricing Documentation Chunks", expanded=True):
            for doc in rag_data.get("pricing_docs", []):
                st.markdown(doc)

        with st.expander("🏆 Case Studies (e.g., Case Study X)", expanded=True):
            for doc in rag_data.get("case_studies", []):
                st.markdown(doc)

        with st.expander("📖 Sales Playbooks", expanded=True):
            for doc in rag_data.get("playbooks", []):
                st.markdown(doc)

    with tab_langgraph:
        st.subheader("State Machine Workflow Graph")
        st.markdown("""
```mermaid
graph TD
    Start([START]) --> Intent[Intent Analyzer Node]
    Intent --> FetchCRM[Fetch CRM Data via MCP]
    FetchCRM -->|Customer Found| RAG[RAG Retrieval Node]
    FetchCRM -->|Customer Not Found| End([END])
    RAG --> Synth[Sales Strategy Synthesizer]
    Synth --> Guard[Compliance Guardrail Node]
    Guard --> End
```
""")
        st.subheader("Execution Trace & State Evolution")
        st.dataframe(result.get("audit_trace", []))
