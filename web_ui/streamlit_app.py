"""Streamlit dashboard for interactive analysis."""
from __future__ import annotations
import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="Stock Analyzer", layout="wide")
st.title("A-share Sector Hotspot Analyzer")


@st.cache_data(ttl=120)
def fetch_latest(limit: int = 20):
    resp = requests.get(f"{API_BASE}/analyses", params={"limit": limit}, timeout=15)
    resp.raise_for_status()
    return resp.json().get("results", [])


def trigger_analysis(trade_date: str | None = None):
    payload = {"trade_date": trade_date} if trade_date else {}
    resp = requests.post(f"{API_BASE}/analyze", json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


col1, col2 = st.columns([2, 1])
with col2:
    trade_date = st.text_input("Trade date (YYYYMMDD)", "")
    if st.button("立即分析", use_container_width=True):
        with st.spinner("正在分析..."):
            result = trigger_analysis(trade_date.strip() or None)
        st.success(f"完成 {result.get('count', 0)} 个板块分析")

with col1:
    st.subheader("最新分析")
    try:
        data = fetch_latest()
        for item in data:
            summary = item.get("summary", {})
            analysis = item.get("analysis", {})
            sector = summary.get("sector", "?")
            st.markdown(f"### {sector} ({summary.get('date', '')})")
            st.json(summary)
            st.write(analysis.get("analysis", ""))
            st.divider()
    except Exception as exc:  # show friendly error
        st.error(f"加载分析结果失败: {exc}")
