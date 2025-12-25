"""FastAPI application entrypoint."""
from __future__ import annotations
import datetime as dt
import logging
from typing import Any, Dict, List, Optional

from fastapi import FastAPI

from config.settings import settings, validate_settings
from modules import data_fetcher, metrics_calculator, ai_analyzer, db_handler, utils

utils.setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI(title="Stock Analyzer", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


def _default_trade_date() -> str:
    return dt.datetime.now().strftime("%Y%m%d")


def run_sector_analysis(trade_date: Optional[str] = None) -> List[Dict[str, Any]]:
    validate_settings()
    date = trade_date or _default_trade_date()

    # Placeholder sector universe. Replace with real sector membership data.
    sector_universe = {
        "Banking": ["000001.SZ", "600036.SH"],
        "Construction": ["000002.SZ", "601668.SH"],
    }

    results: List[Dict[str, Any]] = []
    for sector, symbols in sector_universe.items():
        daily = data_fetcher.fetch_daily_data(symbols, start_date=date, end_date=date)
        money = data_fetcher.fetch_money_flow(symbols, trade_date=date)
        margin = data_fetcher.fetch_margin_data(symbols, trade_date=date)

        news_heat = 0.0  # TODO: integrate real news heat
        score = metrics_calculator.score_sector(daily, money, margin, news_heat)

        summary = {
            "date": date,
            "sector": sector,
            "symbols": symbols,
            "score": score,
            "stats": {
                "count": len(symbols),
                "avg_pct_chg": float(daily["pct_chg"].mean()) if not daily.empty else 0.0,
                "net_mf_vol": float(money["net_mf_vol"].mean()) if not money.empty else 0.0,
            },
        }

        try:
            analysis = ai_analyzer.analyze_sector(sector, summary)
        except Exception as exc:  # surface errors but continue
            logger.error("AI analysis failed for %s: %s", sector, exc)
            analysis = {"sector": sector, "analysis": "AI analysis failed.", "raw": {"error": str(exc)}}

        record = {"summary": summary, "analysis": analysis}
        db_handler.save_sector_analysis(record)
        results.append(record)

    return results


@app.post("/analyze")
def trigger_analysis(payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    trade_date = None
    if payload:
        trade_date = payload.get("trade_date")
    results = run_sector_analysis(trade_date)
    return {"count": len(results), "results": results}


@app.get("/analyses")
def list_analyses(limit: int = 20) -> Dict[str, Any]:
    data = db_handler.latest_analyses(limit=limit)
    return {"count": len(data), "results": data}
