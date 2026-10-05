"""
Enterprise Sales & CRM Model Context Protocol (MCP) Server.
Exposes standard MCP tools for CRM data retrieval over stdio, SSE, and HTTP transports.
"""

import sys
import json
import logging
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from .db import crm_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SalesCRM-MCPServer")

# Initialize FastMCP Server instance
mcp = FastMCP(
    name="Sales-CRM-MCP-Server",
    instructions="Production MCP server exposing enterprise CRM data (Customers, Deals, Interactions, Support Tickets).",
)


@mcp.tool()
def get_customer(customer_name_or_id: str) -> Dict[str, Any]:
    """
    Look up customer profile information from CRM by customer name, alias, or ID.
    Returns customer profile, primary contacts, annual revenue, and health score.
    """
    logger.info(f"MCP Tool Call: get_customer('{customer_name_or_id}')")
    cust = crm_db.find_customer(customer_name_or_id)
    if not cust:
        return {
            "status": "error",
            "message": f"Customer '{customer_name_or_id}' not found in CRM.",
            "data": None,
        }
    return {
        "status": "success",
        "data": cust,
    }


@mcp.tool()
def get_deals(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve active and historical sales pipeline deals for a customer.
    Returns deal titles, values, sales stages, probabilities, and target products.
    """
    logger.info(f"MCP Tool Call: get_deals('{customer_id}')")
    deals = crm_db.get_deals_by_customer(customer_id)
    return {
        "status": "success",
        "customer_id": customer_id,
        "count": len(deals),
        "deals": deals,
    }


@mcp.tool()
def get_previous_interactions(customer_id: str, limit: int = 5) -> Dict[str, Any]:
    """
    Retrieve past sales meetings, emails, executive syncs, and call notes for a customer.
    Sorted from most recent to oldest.
    """
    logger.info(f"MCP Tool Call: get_previous_interactions('{customer_id}', limit={limit})")
    interactions = crm_db.get_interactions_by_customer(customer_id, limit=limit)
    return {
        "status": "success",
        "customer_id": customer_id,
        "count": len(interactions),
        "interactions": interactions,
    }


@mcp.tool()
def get_support_tickets(customer_id: str, status: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve engineering and IT support tickets for a customer.
    Optional status filter: 'OPEN', 'PENDING', 'RESOLVED'.
    Essential for identifying friction before client meetings.
    """
    logger.info(f"MCP Tool Call: get_support_tickets('{customer_id}', status={status})")
    tickets = crm_db.get_support_tickets_by_customer(customer_id, status=status)
    open_count = sum(1 for t in tickets if t.get("status", "").upper() == "OPEN")
    return {
        "status": "success",
        "customer_id": customer_id,
        "total_count": len(tickets),
        "open_count": open_count,
        "tickets": tickets,
    }


def create_starlette_app():
    """
    Returns an ASGI/Starlette app for hosting the MCP server over SSE / HTTP.
    Ideal for deploying on Docker, AWS ECS, GCP Cloud Run, or Kubernetes.
    """
    return mcp.sse_app()


if __name__ == "__main__":
    # If run directly with --sse, run on SSE / Starlette server
    if "--sse" in sys.argv:
        port = 8000
        logger.info(f"Starting MCP Server on SSE transport at http://0.0.0.0:{port}/sse ...")
        mcp.run(transport="sse")
    else:
        # Default standard transport for MCP: stdio
        logger.info("Starting MCP Server on standard stdio transport ...")
        mcp.run(transport="stdio")
