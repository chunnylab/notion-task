import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List


class NotionClient:
    """Minimal Notion API client using python stdlib urllib."""

    BASE_URL = "https://api.notion.com/v1"
    NOTION_VERSION = "2022-06-28"

    def __init__(self, api_key: str | None = None):
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

    def append_block_children(self, block_id: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Append blocks to a page or block container."""
        clean_id = block_id.replace("-", "")
        url = f"{self.BASE_URL}/blocks/{clean_id}/children"
        data = json.dumps({"children": children}).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=self._headers(), method="PATCH")
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            err_body = exc.read().decode("utf-8")
            raise RuntimeError(f"Notion API error (HTTP {exc.code}): {err_body}") from exc
