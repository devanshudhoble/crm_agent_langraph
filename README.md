# Enterprise Sales / CRM Research Agent

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![MCP Standard](https://img.shields.io/badge/protocol-Anthropic%20MCP-purple.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade **Forward Deployed Engineer (FDE)** project demonstrating an autonomous Sales & CRM Research Agent. Built with **LangGraph**, the **Model Context Protocol (MCP)**, and a **Multi-Domain RAG Engine**, this system equips account executives and sales leaders with complete, risk-aware meeting briefings in under 30 seconds.

---

## 📑 Architecture Overview

```
                          Salesperson Natural Language Prompt
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │  LangGraph   │
                                   │ State Machine│
                                   └──────┬───────┘
                                          │
                                          ▼
                        Model Context Protocol (MCP Server)
                     ┌────────────────────┼───────────────────┐
                     ▼                    ▼                   ▼
              get_customer()         get_deals()     get_interactions()
                     │                    │                   │
                     └────────────────────┼───────────────────┘
                                          │
                                          ▼
                                get_support_tickets()
                                          │
                                          ▼
                                 Live CRM Data Layer
                       (Deals: ₹25L | Tickets: 2 Open Issues)
                                          │
                                          ▼
                            Multi-Domain RAG Engine
                  ┌───────────────┬───────────────┬───────────────┐
                  ▼               ▼               ▼               ▼
            Product Docs     Pricing Docs    Case Studies     Playbooks
            (Enterprise AI)  (₹25L Core SLA) (Case Study X)  (CTO Strategy)
                                          │
                                          ▼
                       LangGraph Compliance & Guardrail Check
                        (Prioritize open tickets before pitch)
                                          │
                                          ▼
                             Executive Meeting Briefing
```

---

## 🎯 The Real-World Scenario

### Salesperson Query:
> *"Give me a summary of customer ABC and tell me what I should discuss in tomorrow's meeting."*

### Agent Generated Output:
```markdown
### Executive Account Briefing: ABC Corp

**Customer:** ABC Corp (Financial Services & Banking (BFSI))
**Primary Stakeholder:** Rajesh Sharma (Chief Technology Officer (CTO))

**Current deal:** ₹25,00,000 (₹25L)
**Last interaction:** Sept 28
**Open support issues:** 2
**Interested product:** Enterprise AI

---

### Recommended Discussion Strategy for Tomorrow's Meeting:
1. **Resolve open support issues first**:
   - Proactively address tickets TICK-9021, TICK-9034.
   - Explain scheduled Hotfix v2.4.1 raising webhook timeout ceiling to 120s and SSO renewal update.
     Demonstrating operational accountability builds executive trust before commercial talks.

2. **Discuss Enterprise AI Core Capabilities**:
   - Revisit the architecture questions raised during the Sept 28 sync.
   - Reaffirm P99 < 450ms agentic decision latency and private VPC deployment model covered in ₹25L tier.

3. **Present Case Study X**:
   - Reference our Tier-1 Private Bank deployment where prep time was reduced by 92% and cleared RBI audit.
   - Directly maps to CTO Rajesh Sharma's requirements for enterprise governance.
```

---

## 🔌 Model Context Protocol (MCP) Deep Dive

### 1. Transportation Layer
| Transport | Delivery Mechanism | Deployment Use Case | Framing |
| :--- | :--- | :--- | :--- |
| **stdio** | Standard OS pipes (`stdin`/`stdout`) | Local CLI, desktop agent runtimes, embedded sidecars | Line-delimited JSON-RPC 2.0 |
| **SSE** | Server-Sent Events over HTTP | Microservices, Docker, Kubernetes clusters | W3C SSE event stream + POST |
| **Streamable HTTP** | Chunked Transfer-Encoding | Multi-tenant gateways, reverse proxies | HTTP/1.1 or HTTP/2 chunked |

### 2. Tools Registered in FastMCP
- `get_customer(customer_name_or_id: str)`: Master profile lookup (POC, health score, revenue, tier).
- `get_deals(customer_id: str)`: Active and historical deals (deal stages, values, probabilities).
- `get_previous_interactions(customer_id: str, limit: int)`: Chronological meeting notes, emails, and sync logs.
- `get_support_tickets(customer_id: str, status: Optional[str])`: IT/engineering support tickets with severity and RCA.

### 3. Creation & Hosting Topologies
1. **Local Workstation**:
   ```bash
   # stdio transport
   python -m mcp_server.server

   # SSE transport on port 8000
   python -m mcp_server.server --sse
   ```
2. **Containerized (Docker)**:
   ```bash
   docker build -t sales-crm-mcp .
   docker run -d -p 8000:8000 --name crm-mcp sales-crm-mcp
   ```
3. **Enterprise VPC (AWS ECS / GCP Cloud Run / Kubernetes)**:
   Hosted as an internal sidecar or private microservice behind an Application Load Balancer with mTLS authentication.

---

## 🕸️ LangGraph State Machine Architecture

### State Schema (`SalesAgentState`)
```python
class SalesAgentState(TypedDict):
    user_query: str
    target_customer_name: Optional[str]
    intent: str
    customer_profile: Optional[Dict[str, Any]]
    deals: List[Dict[str, Any]]
    previous_interactions: List[Dict[str, Any]]
    support_tickets: List[Dict[str, Any]]
    rag_context: Dict[str, Any]
    recommended_discussion_agenda: List[str]
    risk_assessment: List[str]
    final_briefing: str
    audit_trace: List[Dict[str, Any]]
    current_step: str
```

### Nodes & Graph Flow
1. **`intent_analyzer_node`**: Extracts customer name entity and query intent.
2. **`fetch_crm_data_node`**: Invokes MCP server tools (`get_customer`, `get_deals`, `get_previous_interactions`, `get_support_tickets`).
3. **`crm_routing_condition` (Conditional Edge)**: Routes to RAG if account exists; short-circuits to END if not found.
4. **`rag_retrieval_node`**: Fetches product documentation, pricing tier (₹25L), Case Study X, and CTO playbook.
5. **`sales_strategy_synthesizer_node`**: Composes the executive briefing and prioritized agenda.
6. **`compliance_guardrail_node`**: Verifies that open tickets are placed as Agenda Item #1 and audits numerical integrity.

---

## 📄 Complete Architecture PDF Document

A publication-grade, 6-page comprehensive architecture document has been compiled and included in the repository:
- **Location**: [`docs/Sales_CRM_Research_Agent_Architecture.pdf`](docs/Sales_CRM_Research_Agent_Architecture.pdf)
- **Includes**: Full MCP transport protocol breakdown, JSON-RPC schema contracts, LangGraph node/edge transition tables, RAG semantic scoring formulas, and production hosting guides.

To re-compile the PDF at any time:
```bash
python generate_architecture_pdf.py
```

---

## 🚀 Quickstart & Execution

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/devanshudhoble32/Crm_agent-.git
cd Crm_agent-

# Install dependencies
pip install -r requirements.txt
```

### 2. Run CLI Demo
```bash
python main.py "Give me a summary of customer ABC and tell me what I should discuss in tomorrow's meeting."
```

### 3. Launch Interactive Streamlit Cockpit
```bash
streamlit run ui/app.py
```

### 4. Run Automated Test Suite
```bash
pytest tests/test_agent.py -v
```

---

## 💼 Business Impact (Why FDE Teams Care)

* **92% Reduction in Meeting Prep Time**: Drops preparation time from 45 minutes across 4 systems to under 30 seconds.
* **Elimination of Critical Blind Spots**: Proactively addresses open support tickets before renewals, preserving executive trust.
* **Pipeline Acceleration**: Automatically arms reps with matching peer validation (**Case Study X**) and accurate commercial packages (**₹25L Enterprise Core**).
* **Guaranteed Audit Integrity**: Deterministic LangGraph guardrails prevent hallucinated discounts and ensure strict banking compliance.
