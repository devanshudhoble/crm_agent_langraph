import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import math


class KnowledgeChunk:
    def __init__(self, doc_name: str, category: str, title: str, content: str):
        self.doc_name = doc_name
        self.category = category  # 'product', 'pricing', 'case_study', 'playbook'
        self.title = title
        self.content = content
        self.words = set(re.findall(r"\w+", (title + " " + content).lower()))

    def score(self, query_terms: List[str]) -> float:
        """
        Calculate BM25-inspired lexical overlap score with length normalization.
        """
        match_count = sum(1 for term in query_terms if term in self.words)
        if match_count == 0:
            return 0.0
        # Title matches receive a 2.5x boost
        title_boost = sum(2.5 for term in query_terms if term in self.title.lower())
        total_score = (match_count + title_boost) / math.sqrt(len(self.words) + 10)
        return total_score


class KnowledgeBaseRetriever:
    """
    Enterprise RAG Retriever supporting document indexing and contextual retrieval
    across Products, Pricing, Case Studies, and Sales Playbooks.
    """

    def __init__(self, kb_dir: Optional[Path] = None):
        if kb_dir is None:
            kb_dir = Path(__file__).parent / "knowledge_base"
        self.kb_dir = kb_dir
        self.chunks: List[KnowledgeChunk] = []
        self._index_documents()

    def _index_documents(self):
        if not self.kb_dir.exists():
            return

        category_map = {
            "products.md": "product",
            "pricing.md": "pricing",
            "case_studies.md": "case_study",
            "sales_playbooks.md": "playbook",
        }

        for file_path in self.kb_dir.glob("*.md"):
            cat = category_map.get(file_path.name, "general")
            content = file_path.read_text(encoding="utf-8")
            self._split_and_index_file(file_path.name, cat, content)

    def _split_and_index_file(self, filename: str, category: str, content: str):
        # Split on markdown section headers (## or ###)
        sections = re.split(r"\n(?=#{2,3}\s)", content)
        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue
            lines = sec.split("\n")
            header_line = lines[0].replace("#", "").strip()
            body = "\n".join(lines[1:]).strip() if len(lines) > 1 else header_line
            chunk = KnowledgeChunk(
                doc_name=filename,
                category=category,
                title=header_line,
                content=sec,
            )
            self.chunks.append(chunk)

    def retrieve(self, query: str, category: Optional[str] = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top_k chunks matching the query string, optionally filtered by category.
        """
        query_terms = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
        if not query_terms:
            return []

        scored = []
        for c in self.chunks:
            if category and c.category != category:
                continue
            score = c.score(query_terms)
            if score > 0:
                scored.append((score, c))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for s, chunk in scored[:top_k]:
            results.append({
                "score": round(s, 3),
                "category": chunk.category,
                "document": chunk.doc_name,
                "title": chunk.title,
                "content": chunk.content,
            })
        return results

    def retrieve_context_for_deal(
        self,
        product_name: str,
        industry: str = "",
        has_tickets: bool = False,
    ) -> Dict[str, Any]:
        """
        Contextually retrieves relevant Product doc, Pricing tier, Case study, and Playbook.
        """
        # 1. Product details
        prod_chunks = self.retrieve(f"{product_name} architecture capabilities latency", category="product", top_k=2)
        # 2. Pricing tier
        pricing_chunks = self.retrieve(f"{product_name} Enterprise Core 25L SLA", category="pricing", top_k=1)
        # 3. Case studies (tailored to industry e.g. BFSI / Banking)
        case_query = f"{industry} Bank BFSI Case Study X compliance prep time"
        case_chunks = self.retrieve(case_query, category="case_study", top_k=1)
        if not case_chunks:
            case_chunks = self.retrieve("Case Study X", category="case_study", top_k=1)
        # 4. Sales playbooks
        playbook_query = "technical decision makers CTO open support tickets Step 1" if has_tickets else "executive alignment"
        playbook_chunks = self.retrieve(playbook_query, category="playbook", top_k=1)

        return {
            "product_docs": [c["content"] for c in prod_chunks],
            "pricing_docs": [c["content"] for c in pricing_chunks],
            "case_studies": [c["content"] for c in case_chunks],
            "playbooks": [c["content"] for c in playbook_chunks],
            "sources": [
                f"{c['document']} ({c['title']})"
                for c in (prod_chunks + pricing_chunks + case_chunks + playbook_chunks)
            ],
        }


kb_retriever = KnowledgeBaseRetriever()
