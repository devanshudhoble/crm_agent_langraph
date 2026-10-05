import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class CRMDatabase:
    """
    In-memory CRM Data Repository loaded from seed JSON.
    Acts as the source of truth for Customer Master, Deals, Interactions, and Support Tickets.
    """

    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            data_path = Path(__file__).parent / "data" / "crm_seed.json"
        self.data_path = data_path
        self._data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.data_path.exists():
            return {
                "customers": [],
                "deals": [],
                "interactions": [],
                "support_tickets": [],
            }
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def find_customer(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Find a customer by ID, exact name, or alias (case-insensitive).
        """
        id_clean = identifier.strip().lower()
        for cust in self._data.get("customers", []):
            if cust.get("id", "").lower() == id_clean:
                return cust
            if cust.get("name", "").lower() == id_clean:
                return cust
            aliases = [a.lower() for a in cust.get("aliases", [])]
            if id_clean in aliases or any(id_clean in a for a in aliases):
                return cust
            # Partial match on customer name
            if id_clean in cust.get("name", "").lower():
                return cust
        return None

    def get_deals_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Return all deals associated with a customer_id.
        """
        cid = customer_id.strip().lower()
        return [
            d for d in self._data.get("deals", [])
            if d.get("customer_id", "").lower() == cid
        ]

    def get_interactions_by_customer(self, customer_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Return historical sales & engineering interactions for a customer.
        Sorted newest first.
        """
        cid = customer_id.strip().lower()
        matches = [
            i for i in self._data.get("interactions", [])
            if i.get("customer_id", "").lower() == cid
        ]
        # Sort by date descending
        matches.sort(key=lambda x: x.get("date", ""), reverse=True)
        return matches[:limit]

    def get_support_tickets_by_customer(
        self, customer_id: str, status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Return support tickets for customer. Optionally filter by status (e.g. 'OPEN').
        """
        cid = customer_id.strip().lower()
        tickets = [
            t for t in self._data.get("support_tickets", [])
            if t.get("customer_id", "").lower() == cid
        ]
        if status:
            stat_clean = status.strip().upper()
            tickets = [t for t in tickets if t.get("status", "").upper() == stat_clean]
        return tickets


# Global singleton instance for high-performance direct execution
crm_db = CRMDatabase()
