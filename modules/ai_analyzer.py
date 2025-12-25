"""SiliconFlow LLM integration for sector analysis."""
from __future__ import annotations
import json
from typing import Any, Dict

import requests

from config.settings import settings

API_URL = "https://api.siliconflow.cn/v1/chat/completions"


def analyze_sector(sector_name: str, summary: Dict[str, Any]) -> Dict[str, Any]:
    if not settings.siliconflow_api_key:
        raise RuntimeError("SILICONFLOW_API_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {settings.siliconflow_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.siliconflow_model or "",
        "messages": [
            {"role": "system", "content": "You are a market analyst focusing on A-share sectors."},
            {
                "role": "user",
                "content": (
                    f"Please analyze A-share sector '{sector_name}'. "
                    f"Here is the aggregated data: {json.dumps(summary, ensure_ascii=False)}. "
                    "Provide a concise technical view and potential risks."
                ),
            },
        ],
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"SiliconFlow API error: {resp.status_code} {resp.text}")

    data = resp.json()
    # Response shape may vary; adjust parsing accordingly.
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {"sector": sector_name, "analysis": content, "raw": data}
