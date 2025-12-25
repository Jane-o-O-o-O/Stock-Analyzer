"""Metrics aggregation and scoring for sectors."""
from __future__ import annotations
import pandas as pd


def _safe_mean(series: pd.Series) -> float:
    return float(series.mean()) if not series.empty else 0.0


def score_sector(daily: pd.DataFrame, money: pd.DataFrame, margin: pd.DataFrame, news_heat: float = 0.0) -> float:
    """Compute a composite score for a sector given multiple indicators."""
    if daily.empty:
        return 0.0

    vol_score = _safe_mean(daily.get("vol", pd.Series()))
    amt_score = _safe_mean(daily.get("amount", pd.Series()))
    pct_score = _safe_mean(daily.get("pct_chg", pd.Series()))
    money_score = _safe_mean(money.get("net_mf_vol", pd.Series())) if not money.empty else 0.0
    margin_score = _safe_mean(margin.get("fin_bal", pd.Series())) if not margin.empty else 0.0

    # Normalize rough magnitudes for a simple heuristic score
    score = (
        pct_score * 0.35 +
        money_score * 0.25 +
        vol_score * 0.15 +
        amt_score * 0.1 +
        margin_score * 0.1 +
        news_heat * 0.05
    )
    return float(score)


def rank_sectors(scores: dict, top_n: int = 10):
    return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
