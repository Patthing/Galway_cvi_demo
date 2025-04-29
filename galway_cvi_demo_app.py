"""
Streamlit Demo – Galway Cultural Value Index (offline mock‑up)
=============================================================
All numbers are hard‑coded so no external data or API keys are needed.
Edit the lists in `data = {...}` or replace with a CSV read when you want
real figures.

Run locally:
    pip install streamlit
    streamlit run galway_cvi_demo_app.py

Or deploy on Streamlit Cloud: upload this single file and click Deploy.
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
from math import prod

# -------------------- sample data 2015‑2024 --------------------
years = list(range(2015, 2025))
data = {
    "Year": years,
    "cultural_vibrancy": [0.45, 0.47, 0.48, 0.50, 0.53, 0.51, 0.56, 0.58, 0.60, 0.62],
    "creative_economy":   [0.35, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52],
    "enabling_env":       [0.40, 0.41, 0.42, 0.44, 0.46, 0.47, 0.49, 0.51, 0.53, 0.55],
}
df = pd.DataFrame(data).set_index("Year")

# headline CVI = geometric mean
parts = ["cultural_vibrancy", "creative_economy", "enabling_env"]
df["CVI"] = [
    prod([(row[p] + 1) for p in parts]) ** (1/len(parts)) - 1
    for _, row in df.iterrows()
]

# -------------------- Streamlit UI ------------------------------
st.set_page_config(page_title="Galway CVI demo", layout="wide")
st.title("Galway Cultural Value Index – Demo Dashboard")

st.markdown("This demo uses static mock data. Replace the numbers in the code with real data when you're ready.")

st.sidebar.header("Options")
yr_from, yr_to = st.sidebar.select_slider(
    "Year range", options=years, value=(years[0], years[-1])
)
columns = st.sidebar.multiselect(
    "Lines to plot",
    ["cultural_vibrancy", "creative_economy", "enabling_env", "CVI"],
    default=["CVI"],
)

view = df.loc[yr_from:yr_to, columns]
st.line_chart(view)
st.dataframe(view.style.format("{:.3f}"))
st.download_button(
    "Download CSV",
    view.reset_index().to_csv(index=False).encode(),
    "galway_cvi_demo.csv",
    "text/csv",
)

st.caption("Offline demo • no external calls • v0.1")
