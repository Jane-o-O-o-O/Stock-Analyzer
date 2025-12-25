"""MongoDB helpers for persisting analyses."""
from __future__ import annotations
import datetime as dt
from functools import lru_cache
from typing import Any, Dict, List

from pymongo import MongoClient

from config.settings import settings


@lru_cache(maxsize=1)
def _get_client() -> MongoClient:
    return MongoClient(settings.mongodb_uri)


def get_collection(name: str):
    client = _get_client()
    return client[settings.mongodb_db][name]


def save_sector_analysis(record: Dict[str, Any]) -> None:
    record["created_at"] = dt.datetime.utcnow()
    col = get_collection("sector_analysis")
    col.insert_one(record)


def latest_analyses(limit: int = 20) -> List[Dict[str, Any]]:
    col = get_collection("sector_analysis")
    cursor = col.find().sort("created_at", -1).limit(limit)
    return list(cursor)
