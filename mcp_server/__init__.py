"""
MCP Server package for Sales & CRM data integration.
Exposes Model Context Protocol tools for customer master, deals, interactions, and tickets.
"""

from .db import CRMDatabase
from .server import mcp, create_starlette_app

__all__ = ["CRMDatabase", "mcp", "create_starlette_app"]
