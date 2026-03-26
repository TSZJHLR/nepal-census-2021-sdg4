import json
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, State

def load_all_data():
    try:
        with open("data/npl_admin1.geojson") as f:
            prov_geo = json.load(f)
        with open("data/npl_admin2.geojson") as f:
            dist_geo = json.load(f)
    except FileNotFoundError:
        prov_geo, dist_geo = {"type": "FeatureCollection", "features": []}, {"type": "FeatureCollection", "features": []}

    try:
        df_raw = pd.read_csv("data/nepal-census-dataset.csv")
        metrics = ["avg_literacy_rate", "avg_dropout_rate", "avg_infrastructure_score", "avg_trained_teachers_pct"]

        df = df_raw.groupby(["district", "province"])[metrics].mean().reset_index()
        return prov_geo, dist_geo, df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return prov_geo, dist_geo, pd.DataFrame()

PROV_GEO, DIST_GEO, DF_STATS = load_all_data()

METRICS = {
    "avg_literacy_rate": {"label": "Literacy Rate (%)", "colorscale": "Blues"},
    "avg_dropout_rate": {"label": "Dropout Rate (%)", "colorscale": "Reds"},
    "avg_infrastructure_score": {"label": "Infrastructure Score", "colorscale": "Greens"},
    "avg_trained_teachers_pct": {"label": "Trained Teachers (%)", "colorscale": "Purples"}
}