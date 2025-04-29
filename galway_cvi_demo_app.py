"""
Streamlit Demo – Galway Cultural Value Index (offline mock‑up, 5 indicators)
===========================================================================
This single‑file Streamlit app shows what the finished dashboard will look
like using **five** proxy indicators and invented numbers for 2015‑2024.

Indicators included
-------------------
1. Employment in creative industries  (persons)
2. Cultural infrastructure            (libraries, cinemas, theatres, etc.)
3. Festivals in the region            (annual count)
4. Movies produced in Galway          (feature + TV seasons)
5. YouTube uploads from Galway        (public uploads tagged to the county)

The headline CVI is the **simple average of each indicator linearly scaled to
0‑1** across the 10‑year window – good enough for a demo while conveying the
idea of normalisation.

Usage
-----
• **Locally**   `pip install streamlit` then `streamlit run galway_cvi_demo_app.py`
• **Cloud**     Upload this file to GitHub → Deploy on Streamlit Cloud → Done.

Swap the lists under `proxy_data` for real numbers or replace the whole block
with `pd.read_csv()` when actual datasets are ready.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# 1️⃣  Proxy data (edit these lists or load from a CSV later)
# ---------------------------------------------------------------------------

years = list(range(2015, 2025))
proxy_data = {
    "Year": years,
    "employment_creative": [1100, 1120, 1140, 1170, 1200, 1230, 1270, 1310, 1360, 1420],
    "cultural_infrastructure": [25, 25, 26, 26, 27, 28, 29, 30, 31, 32],
    "festivals": [11, 11, 12, 12, 13, 14, 14, 15, 16, 17],
    "movies_made": [2, 2, 3, 3, 3, 4, 4, 5, 5, 6],
    "youtube_uploads": [220, 230, 240, 260, 280, 300, 330, 360, 400, 450],
}

df_raw = pd.DataFrame(proxy_data).set_index("Year")

# ---------------------------------------------------------------------------
# 2️⃣  Normalise 0‑1 and compute CVI = mean of five scaled series
# ---------------------------------------------------------------------------

def min_max(series: pd.Series) -> pd.Series:
    return (series - series.min()) / (series.max() - series.min())

scaled = df_raw.apply(min_max, axis=0).rename(columns={
    "employment_creative": "Employment in creative industries",
    "cultural_infrastructure": "Cultural infrastructure",
    "festivals": "Festivals",
    "movies_made": "Movies made",
    "youtube_uploads": "YouTube uploads",
})
scaled["CVI"] = scaled.mean(axis=1)

# ---------------------------------------------------------------------------
# 3️⃣  Streamlit UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Galway CVI demo (5 indicators)", layout="wide")
st.title("Galway Cultural Value Index – Demo (5 indicators)")

st.markdown("This demo uses synthetic numbers for 2015‑2024 so you can explore the interface without external data.")

st.sidebar.header("Options")
start, end = st.sidebar.select_slider(
    "Year range", options=years, value=(years[0], years[-1])
)
cols_available = list(scaled.columns)
default_cols = ["CVI"]
selected_cols = st.sidebar.multiselect("Lines to plot", cols_available, default=default_cols)

view = scaled.loc[start:end, selected_cols]
st.line_chart(view)

st.dataframe(view.style.format("{:.2f}"))
st.download_button(
    "Download CSV (demo numbers)", view.reset_index().to_csv(index=False).encode(), "galway_cvi_demo.csv", "text/csv",
)

st.caption("Offline demo • 5 proxy indicators • v0.2 – replace lists in the code with real data when ready.")
