from dash import dcc, html
import dash_bootstrap_components as dbc
from .engine import METRICS

NEPAL_GRADIENT = {
    "background": "linear-gradient(135deg, #DC143C 15%, #FFFFFF 50%, #003893 85%)",
    "backgroundAttachment": "fixed",
    "minHeight": "100vh",
    "fontFamily": "Segoe UI, Arial"
}

layout = html.Div(style=NEPAL_GRADIENT, children=[
    dbc.Container([
        dcc.Store(id='current-view', data={'level': 'province', 'filter': None}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2("Nepal Edu", className="text-center py-3"),
                    html.Hr(),
                    html.Label("Select Metric:", className="fw-bold"),
                    dcc.Dropdown(
                        id="metric-selector",
                        options=[{"label": v["label"], "value": k} for k, v in METRICS.items()],
                        value=None,
                        placeholder="--- Select a Metric ---",
                        clearable=False
                    ),
                    html.Div(id="back-btn-container", children=[
                        html.Button(id={"type": "back-btn", "index": "main"}, style={"display": "none"})
                    ], className="mt-4 text-center")
                ], style={"backgroundColor": "rgba(255,255,255,0.9)", "padding": "20px", "borderRadius": "15px", "height": "90vh", "boxShadow": "0 4px 15px rgba(0,0,0,0.2)"})
            ], width=3),

            dbc.Col([
                dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                    dcc.Tab(label='Geospatial Map', value='tab-1', children=[
                        html.Div([
                            dcc.Graph(id="choropleth-map", style={"height": "75vh"})
                        ], style={"backgroundColor": "white", "padding": "20px", "borderRadius": "0 0 15px 15px"})
                    ]),
                    dcc.Tab(label='Data Tabletop', value='tab-2', children=[
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Regional Breakdown", className="mb-3"),
                                    html.Div(id="data-table-container")
                                ], width=12, className="mb-4"),
                                dbc.Col([
                                    html.H5("Metric Comparison", className="mb-3"),
                                    dcc.Graph(id="side-bar-chart", style={"height": "40vh"})
                                ], width=12)
                            ])
                        ], style={"backgroundColor": "white", "padding": "30px", "borderRadius": "0 0 15px 15px", "minHeight": "75vh"})
                    ]),
                ], colors={"border": "white", "primary": "#003893", "background": "#f8f9fa"})
            ], width=9)
        ], className="pt-4")
    ], fluid=True)
])