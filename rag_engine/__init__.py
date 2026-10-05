"""
RAG Engine package for Sales & CRM research agent.
Provides semantic & hybrid retrieval across Products, Pricing, Case Studies, and Playbooks.
"""

from .retriever import KnowledgeBaseRetriever, kb_retriever

__all__ = ["KnowledgeBaseRetriever", "kb_retriever"]
