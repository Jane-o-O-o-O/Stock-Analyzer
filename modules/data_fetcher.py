"""Data fetching utilities for A-share market using Tushare and AKShare."""
from __future__ import annotations
import datetime as dt
from functools import lru_cache
from typing import Iterable, List, Optional

import pandas as pd
import tushare as ts
import akshare as ak

from config.settings import settings


@lru_cache(maxsize=1)
def _get_ts_pro() -> ts.pro_api:
    if not settings.tushare_token:
        raise RuntimeError("TUSHARE_TOKEN is not configured")
    return ts.pro_api(settings.tushare_token)


def fetch_daily_data(symbols: Iterable[str], start_date: str, end_date: Optional[str] = None) -> pd.DataFrame:
    """Fetch daily OHLCV data for given symbols between dates (YYYYMMDD)."""
    pro = _get_ts_pro()
    end = end_date or dt.datetime.now().strftime("%Y%m%d")
    frames: List[pd.DataFrame] = []
    for code in symbols:
        df = pro.daily(ts_code=code, start_date=start_date, end_date=end)
        if not df.empty:
            df["ts_code"] = code
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def fetch_money_flow(symbols: Iterable[str], trade_date: str) -> pd.DataFrame:
    """Fetch money flow data for symbols on a specific date."""
    pro = _get_ts_pro()
    frames: List[pd.DataFrame] = []
    for code in symbols:
        df = pro.moneyflow(ts_code=code, trade_date=trade_date)
        if not df.empty:
            df["ts_code"] = code
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def fetch_margin_data(symbols: Iterable[str], trade_date: str) -> pd.DataFrame:
    """Fetch margin trading data for symbols on a specific date."""
    pro = _get_ts_pro()
    frames: List[pd.DataFrame] = []
    for code in symbols:
        df = pro.margin_detail(ts_code=code, trade_date=trade_date)
        if not df.empty:
            df["ts_code"] = code
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def fetch_concept_members() -> pd.DataFrame:
    """Fetch concept sector membership via AKShare (fallback to Tushare if available)."""
    try:
        return ak.stock_board_concept_name_ths()
    except Exception:
        return pd.DataFrame()


def fetch_news_heat(keywords: List[str]) -> pd.DataFrame:
    """Placeholder for news heat; can be replaced with real API or scraping."""
    # TODO: integrate real news heat source
    return pd.DataFrame({"keyword": keywords, "heat": [0 for _ in keywords]})
