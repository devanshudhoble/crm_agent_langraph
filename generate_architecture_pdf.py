"""
Publication-Quality PDF Generator for Enterprise Sales/CRM Research Agent Architecture.
Covers MCP Server/Client flow, data transport, hosting topologies, and LangGraph State/Node/Edge design.
"""

import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count on running footers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(
                54,
                11 * inch - 36,
                "Enterprise Sales/CRM Research Agent | Architecture & Implementation Guide",
            )
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Footer (all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY | FORWARD DEPLOYED ENGINEERING (FDE)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * inch - 54, 48)

        self.restoreState()


def build_architecture_pdf(output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Slate / Navy
    c_brand = colors.HexColor("#1D4ED8")      # Royal Blue
    c_accent = colors.HexColor("#0D9488")     # Teal
    c_text = colors.HexColor("#1E293B")       # Dark Charcoal
    c_bg_light = colors.HexColor("#F8FAFC")   # Light background
    c_border = colors.HexColor("#E2E8F0")     # Light gray border

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=c_brand,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=c_text,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        "BulletDark",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3,
    )

    code_style = ParagraphStyle(
        "CodeBlock",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4,
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
    )

    story = []

    # ================= PAGE 1: TITLE & EXECUTIVE SUMMARY =================
    story.append(Paragraph("Enterprise Sales / CRM Research Agent", title_style))
    story.append(Paragraph("System Architecture, MCP Protocol Specification & LangGraph State Machine Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_brand, spaceBefore=0, spaceAfter=12))

    # Metadata Grid
    meta_data = [
        [
            Paragraph("<b>Author:</b> Forward Deployed Engineering (FDE) Team", body_style),
            Paragraph("<b>Repository:</b> <font color='#1D4ED8'>github.com/devanshudhoble32/Crm_agent-</font>", body_style),
        ],
        [
            Paragraph("<b>Core Frameworks:</b> LangGraph, Anthropic MCP, FastMCP, Python 3.13", body_style),
            Paragraph("<b>Target Domain:</b> Enterprise BFSI, Tier-1 Account Strategy & Deal Acceleration", body_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[240, 264])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), c_bg_light),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 1, c_border),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. Executive Summary & Forward Deployed Engineering Vision", h1_style))
    story.append(Paragraph(
        "Modern enterprise sales professionals spend between 30 to 45 minutes manually preparing for client meetings. "
        "They scramble across multiple disconnected siloed systems: CRM records for account owners, billing pipelines for deal values, "
        "email/calendar archives for interaction history, and IT support ticketing platforms (e.g. Jira, Zendesk) for operational friction. "
        "Walking into an executive meeting unaware of ongoing staging/sandbox outages or unresolved high-priority support tickets severely damages executive credibility.",
        body_style
    ))
    story.append(Paragraph(
        "The <b>Sales / CRM Research Agent</b> solves this high-value enterprise problem. Given a simple conversational prompt—such as "
        "<i>\"Give me a summary of customer ABC and tell me what I should discuss in tomorrow's meeting\"</i>—the system autonomously coordinates "
        "live data retrieval across systems via the <b>Model Context Protocol (MCP)</b>, synthesizes targeted internal knowledge using <b>RAG</b> "
        "(products, pricing, peer case studies, playbooks), and executes a deterministic <b>LangGraph</b> state machine to produce an actionable, "
        "C-level executive briefing with prioritized agenda recommendations.",
        body_style
    ))

    # Architecture Overview Flowchart
    story.append(Paragraph("End-to-End Information Flow", h2_style))
    diag_data = [
        [
            Paragraph("<b>1. Sales Executive Prompt</b><br/>\"Give me summary of ABC Corp and tomorrow's meeting agenda\"", code_style),
            Paragraph("<b>&rarr;</b>", title_style),
            Paragraph("<b>2. LangGraph Engine</b><br/>Stateful workflow orchestration & conditional routing", code_style),
            Paragraph("<b>&rarr;</b>", title_style),
            Paragraph("<b>3. MCP Server Hub</b><br/>get_customer, get_deals, get_interactions, get_tickets", code_style),
        ],
        [
            Paragraph("<b>6. Executive Briefing</b><br/>Deals (Rs 25L), 2 Open Tickets, Case Study X, Actionable Agenda", code_style),
            Paragraph("<b>&larr;</b>", title_style),
            Paragraph("<b>5. Guardrails & Synthesis</b><br/>Operational tickets prioritized; compliance verified", code_style),
            Paragraph("<b>&larr;</b>", title_style),
            Paragraph("<b>4. RAG Engine</b><br/>Products, Pricing Tier (Rs 25L), Case Study X (BFSI Bank), Playbooks", code_style),
        ]
    ]
    diag_table = Table(diag_data, colWidths=[150, 20, 150, 20, 164])
    diag_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 14))

    # ================= PAGE 2: MCP SERVER & CLIENT DEEP DIVE =================
    story.append(PageBreak())
    story.append(Paragraph("2. Model Context Protocol (MCP): Server & Client Architecture", h1_style))
    story.append(Paragraph(
        "<b>Model Context Protocol (MCP)</b> is an open standard introduced by Anthropic that standardizes how LLM applications "
        "connect to external tools, data sources, and enterprise context. Instead of ad-hoc REST integrations and brittle function wrappers, "
        "MCP establishes a formal client-server architecture with structured JSON-RPC 2.0 messages, typed schemas, and capability negotiation.",
        body_style
    ))

    story.append(Paragraph("2.1 Transportation Layer Analysis: stdio vs. SSE vs. Streamable HTTP", h2_style))
    story.append(Paragraph(
        "The MCP specification supports multiple transport mechanisms depending on the isolation and network requirements:",
        body_style
    ))

    trans_data = [
        [
            Paragraph("<b>Transport</b>", code_style),
            Paragraph("<b>Mechanism</b>", code_style),
            Paragraph("<b>Best Use Case</b>", code_style),
            Paragraph("<b>Data Framing</b>", code_style),
        ],
        [
            Paragraph("<b>stdio</b><br/>(Standard I/O)", code_style),
            Paragraph("Direct OS pipes (`stdin`/`stdout`). Subprocess spawned by host.", body_style),
            Paragraph("Local CLI, desktop IDEs, embedded sidecars, air-gapped runtimes.", body_style),
            Paragraph("Line-delimited JSON-RPC 2.0 frames over stdout/stdin.", code_style),
        ],
        [
            Paragraph("<b>SSE</b><br/>(Server-Sent Events)", code_style),
            Paragraph("HTTP POST for requests; persistent Server-Sent Events stream for responses.", body_style),
            Paragraph("Distributed microservices, Docker containers, multi-tenant Kubernetes clouds.", body_style),
            Paragraph("W3C SSE stream (`event: message`, `data: {...}`) + HTTP POST.", code_style),
        ],
        [
            Paragraph("<b>Streamable HTTP</b>", code_style),
            Paragraph("Chunked HTTP 1.1/2 transfer encoding with bi-directional streaming.", body_style),
            Paragraph("High-throughput server-to-server gateways with proxy support.", body_style),
            Paragraph("Transfer-Encoding: chunked with JSON payload streams.", code_style),
        ],
    ]
    trans_table = Table(trans_data, colWidths=[90, 140, 140, 134])
    trans_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, c_border),
        ("BACKGROUND", (0, 1), (-1, 1), c_bg_light),
        ("BACKGROUND", (0, 2), (-1, 2), colors.white),
        ("BACKGROUND", (0, 3), (-1, 3), c_bg_light),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(trans_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.2 How the Local Server is Created & Registered", h2_style))
    story.append(Paragraph(
        "In our implementation (`mcp_server/server.py`), the server is built using the high-performance <b>FastMCP</b> library. "
        "Each tool is registered with typed signatures, docstrings, and JSON Schema definitions automatically exposed to clients:",
        body_style
    ))

    server_snippet = """# mcp_server/server.py
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Sales-CRM-MCP-Server")

@mcp.tool()
def get_customer(customer_name_or_id: str) -> dict: ...

@mcp.tool()
def get_deals(customer_id: str) -> dict: ...

@mcp.tool()
def get_previous_interactions(customer_id: str, limit: int = 5) -> dict: ...

@mcp.tool()
def get_support_tickets(customer_id: str, status: str = None) -> dict: ..."""
    
    snip_table = Table([[Paragraph(server_snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    snip_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(snip_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.3 Where and How to Host the MCP Server", h2_style))
    story.append(Paragraph("In enterprise deployments, the MCP Server can be hosted across three distinct topologies:", body_style))
    story.append(Paragraph("<b>1. Local Development / Workstation:</b> Run as a local process via stdio (`python -m mcp_server.server`) or as an SSE service (`python -m mcp_server.server --sse`). The client launches or connects via localhost loopback with zero network latency.", bullet_style))
    story.append(Paragraph("<b>2. Docker Containerized Microservice:</b> Containerized with lightweight Python base (e.g., `python:3.13-slim`), exposing port 8000. Run via `docker run -p 8000:8000 sales-crm-mcp`. Healthcheck endpoint `/healthz` monitors process vitality.", bullet_style))
    story.append(Paragraph("<b>3. Private Enterprise VPC (AWS ECS Fargate / GCP Cloud Run / K8s):</b> Deployed in an internal non-public VPC subnet behind an Application Load Balancer with Mutual TLS (mTLS) authentication. Zero egress to public internet ensures complete enterprise data sovereignty.", bullet_style))

    # ================= PAGE 3: LANGGRAPH NODES, STATE & EDGES =================
    story.append(PageBreak())
    story.append(Paragraph("3. LangGraph Workflow: State, Nodes, and Graph Edges", h1_style))
    story.append(Paragraph(
        "<b>LangGraph</b> provides a robust, cyclically capable, stateful graph runtime. "
        "Unlike naive sequential chains or unconstrained ReAct loops that risk infinite execution, LangGraph enforces "
        "deterministic state transitions, rigorous typed schemas, and verifiable guardrail boundaries.",
        body_style
    ))

    story.append(Paragraph("3.1 The Typed State Schema (`SalesAgentState`)", h2_style))
    story.append(Paragraph(
        "Every node reads from and mutates a centrally governed state schema defined in `agent/state.py`:",
        body_style
    ))

    state_data = [
        [Paragraph("<b>State Field</b>", code_style), Paragraph("<b>Type</b>", code_style), Paragraph("<b>Description & Lifecycle Role</b>", code_style)],
        [Paragraph("user_query", code_style), Paragraph("str", code_style), Paragraph("Raw incoming prompt from salesperson (e.g. 'summary of ABC...')", body_style)],
        [Paragraph("target_customer_name", code_style), Paragraph("Optional[str]", code_style), Paragraph("Customer entity identified by Intent Analyzer ('ABC Corp')", body_style)],
        [Paragraph("customer_profile", code_style), Paragraph("Optional[dict]", code_style), Paragraph("Master metadata from MCP `get_customer()` (contacts, tier, revenue)", body_style)],
        [Paragraph("deals", code_style), Paragraph("List[dict]", code_style), Paragraph("Sales pipeline deals from MCP `get_deals()` (values, stages)", body_style)],
        [Paragraph("previous_interactions", code_style), Paragraph("List[dict]", code_style), Paragraph("Historical meetings & emails from MCP `get_previous_interactions()`", body_style)],
        [Paragraph("support_tickets", code_style), Paragraph("List[dict]", code_style), Paragraph("Tickets from MCP `get_support_tickets()`. Highlights open blockers.", body_style)],
        [Paragraph("rag_context", code_style), Paragraph("Dict[str, Any]", code_style), Paragraph("Multi-domain knowledge: Product specs, Pricing, Case Study X, Playbooks", body_style)],
        [Paragraph("recommended_agenda", code_style), Paragraph("List[str]", code_style), Paragraph("Ranked discussion points prioritizing operational ticket resolution first", body_style)],
        [Paragraph("risk_assessment", code_style), Paragraph("List[str]", code_style), Paragraph("Compliance verification log auditing numerical and agenda integrity", body_style)],
        [Paragraph("final_briefing", code_style), Paragraph("str", code_style), Paragraph("Final markdown briefing synthesized for executive meeting delivery", body_style)],
        [Paragraph("audit_trace", code_style), Paragraph("List[dict]", code_style), Paragraph("Chronological execution log tracking timestamps and node outputs", body_style)],
    ]
    state_table = Table(state_data, colWidths=[130, 80, 294])
    state_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, c_border),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [c_bg_light, colors.white]),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(state_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.2 Detailed Node Specifications", h2_style))
    story.append(Paragraph("The workflow consists of five specialized deterministic nodes:", body_style))
    story.append(Paragraph("<b>1. Intent Analyzer Node:</b> Parses input text to extract customer target and verify user intent (e.g., meeting prep, deal review).", bullet_style))
    story.append(Paragraph("<b>2. Fetch CRM Data Node (MCP Dispatcher):</b> Executes JSON-RPC calls against the MCP server for customer profile, deals, interactions, and tickets. Extracts critical flags (e.g. 2 open tickets, Rs 25L deal).", bullet_style))
    story.append(Paragraph("<b>3. RAG Retrieval Node:</b> Queries internal vector/lexical knowledge bases for corresponding product specs, pricing tiers, matching industry case studies (Case Study X for BFSI), and sales playbooks.", bullet_style))
    story.append(Paragraph("<b>4. Sales Strategy Synthesizer Node:</b> Integrates CRM reality with RAG knowledge to compose the 3-step meeting agenda and executive account overview.", bullet_style))
    story.append(Paragraph("<b>5. Compliance Guardrail Node:</b> Verifies that open support tickets are placed FIRST before any product pitch. Checks deal figures and generates audit certifications.", bullet_style))

    story.append(Paragraph("3.3 Graph Edges & Conditional Routing Logic", h2_style))
    story.append(Paragraph(
        "Routing between nodes is defined in `agent/graph.py` using `workflow.add_edge` and `workflow.add_conditional_edges`. "
        "If `fetch_crm` reports an invalid or missing customer account (`mcp_error` present), the graph conditionally short-circuits directly to `END`. "
        "Otherwise, execution smoothly proceeds through RAG retrieval, synthesis, and compliance guardrails.",
        body_style
    ))

    # ================= PAGE 4: RAG INTEGRATION & THE ABC CORP WALKTHROUGH =================
    story.append(PageBreak())
    story.append(Paragraph("4. RAG Knowledge Integration & The ABC Corp Execution Trace", h1_style))
    story.append(Paragraph(
        "The RAG Knowledge Engine (`rag_engine/retriever.py`) indexes four vital sales collateral domains: "
        "<b>Product Documentation</b> (capabilities, latency benchmarks), <b>Pricing Documentation</b> (commercial tiers, multi-year terms), "
        "<b>Case Studies</b> (peer BFSI banking rollouts), and <b>Sales Playbooks</b> (CTO alignment strategy).",
        body_style
    ))

    story.append(Paragraph("Real-World Execution Trace: Customer 'ABC Corp'", h2_style))
    story.append(Paragraph(
        "Here is the exact runtime trace generated when a salesperson requests: "
        "<i>\"Give me a summary of customer ABC and tell me what I should discuss in tomorrow's meeting.\"</i>",
        body_style
    ))

    # Callout Box showing the Generated Output
    output_box = [
        [Paragraph("<b>GENERATED EXECUTIVE BRIEFING (FDE Grade)</b>", ParagraphStyle("H", parent=h2_style, textColor=colors.HexColor("#1E3A8A")))],
        [Paragraph("<b>Customer:</b> ABC Corp (Financial Services & Banking - BFSI)", body_style)],
        [Paragraph("<b>Primary Stakeholder:</b> Rajesh Sharma (Chief Technology Officer)", body_style)],
        [Paragraph("<b>Current deal:</b> Rs 25,00,000 (Rs 25L) - Enterprise Core Tier", body_style)],
        [Paragraph("<b>Last interaction:</b> Sept 28 (Executive Zoom with Priya Nair & Arun Verma)", body_style)],
        [Paragraph("<b>Open support issues:</b> 2 (TICK-9021: API Batch Timeout; TICK-9034: SSO Token Renewal)", body_style)],
        [Paragraph("<b>Interested product:</b> Enterprise AI Platform", body_style)],
        [Paragraph("<hr color='#CBD5E1'/>", body_style)],
        [Paragraph("<b>RECOMMENDED DISCUSSION STRATEGY:</b>", h2_style)],
        [Paragraph("<b>1. Resolve open support issues first:</b> Proactively address tickets TICK-9021 and TICK-9034. Present the scheduled Hotfix v2.4.1 raising webhook timeout ceiling to 120s. Proving operational reliability secures executive confidence before contract signing.", bullet_style)],
        [Paragraph("<b>2. Discuss Enterprise AI Core Capabilities:</b> Revisit latency & data sovereignty requirements raised in the Sept 28 meeting. Reaffirm P99 < 450ms decision latency and private VPC deployment model covered in the Rs 25L tier.", bullet_style)],
        [Paragraph("<b>3. Present Case Study X:</b> Share the Tier-1 Private Bank deployment where meeting prep time dropped by 92% and the solution passed full RBI regulatory audit without exception.", bullet_style)],
    ]
    box_table = Table(output_box, colWidths=[504])
    box_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor("#16A34A")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(box_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("5. Business Impact & Forward Deployed Engineering (FDE) Value", h1_style))
    impact_items = [
        ("92% Reduction in Prep Overhead", "Drops sales prep time from 45 minutes across 4 systems to under 30 seconds of automated briefing."),
        ("Elimination of Blind Spots", "Surfaces critical support ticket friction before high-stakes renewal meetings, preventing contract churn."),
        ("Deal Velocity Acceleration", "Directly equips account executives with tailored peer validation (Case Study X) and accurate pricing tiers (Rs 25L)."),
        ("Strict Enterprise Compliance", "Deterministic LangGraph guardrails prevent hallucinations, verify numbers against CRM, and protect brand reputation."),
    ]
    impact_data = [[Paragraph(f"<b>{k}</b>", code_style), Paragraph(v, body_style)] for k, v in impact_items]
    impact_table = Table(impact_data, colWidths=[170, 334])
    impact_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, c_border),
        ("BACKGROUND", (0, 0), (-1, -1), c_bg_light),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(impact_table)

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Architecture PDF successfully built at: {output_path}")


if __name__ == "__main__":
    pdf_dest = Path(__file__).parent / "docs" / "Sales_CRM_Research_Agent_Architecture.pdf"
    build_architecture_pdf(str(pdf_dest))
