import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


class NotionClient:
    """Minimal Notion API client using python stdlib urllib with zero dependencies."""

    BASE_URL = "https://api.notion.com/v1"
    NOTION_VERSION = "2022-06-28"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "Missing Notion API Key. Set NOTION_API_KEY environment variable or pass api_key."
            )

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": self.NOTION_VERSION,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        body = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=body, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                res_text = resp.read().decode("utf-8")
                return json.loads(res_text) if res_text else {}
        except urllib.error.HTTPError as exc:
            err_body = exc.read().decode("utf-8")
            raise RuntimeError(f"Notion API error (HTTP {exc.code} for {method} {endpoint}): {err_body}") from exc

    def create_page(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a page in a database or parent page."""
        return self._request("POST", "/pages", payload)

    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Update properties of an existing page."""
        clean_id = page_id.replace("-", "")
        return self._request("PATCH", f"/pages/{clean_id}", {"properties": properties})

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Retrieve page metadata and properties."""
        clean_id = page_id.replace("-", "")
        return self._request("GET", f"/pages/{clean_id}")

    def query_database(self, database_id: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Query a database with filter and sort criteria."""
        clean_id = database_id.replace("-", "")
        return self._request("POST", f"/databases/{clean_id}/query", payload or {})

    def append_block_children(self, block_id: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Append blocks to a page or block container."""
        clean_id = block_id.replace("-", "")
        return self._request("PATCH", f"/blocks/{clean_id}/children", {"children": children})
