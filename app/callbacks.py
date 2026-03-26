import plotly.graph_objects as go
import plotly.express as px
from dash import Input, Output, State, dash_table, html, callback_context
from . import dash_app
from .engine import PROV_GEO, DIST_GEO, DF_STATS, METRICS

@dash_app.callback(
    [Output("choropleth-map", "figure"),
     Output("data-table-container", "children"),
     Output("side-bar-chart", "figure"),
     Output("back-btn-container", "children"),
     Output("current-view", "data")],
    [Input("choropleth-map", "clickData"),
     Input("metric-selector", "value"),
     Input({"type": "back-btn", "index": "main"}, "n_clicks")],
    [State("current-view", "data")],
    prevent_initial_call=True
)
def update_dashboard(clickData, selected_metric, n_clicks, current_view):
    ctx = callback_context

    if not ctx.triggered:
        return dash_app.no_update
    
    trigger = ctx.triggered[0]['prop_id']

    # drill-down logic
    view_level = current_view['level']
    target_filter = current_view['filter']

    if 'back-btn' in trigger:
        view_level, target_filter = "province", None
    elif "choropleth-map" in trigger and clickData and view_level == "province":
        view_level, target_filter = "district", clickData['points'][0]['location']

    # filter data
    if view_level == "province":
        dff = DF_STATS.groupby("province")[selected_metric].mean().reset_index()
        geo, loc, f_id = PROV_GEO, dff["province"], "properties.adm1_name"
    else:
        dff = DF_STATS[DF_STATS["province"] == target_filter]
        geo, loc, f_id = DIST_GEO, dff["district"], "properties.adm2_name"

    # fig_map = go.Figure(go.Choroplethmap(
    #     geojson=geo, locations=loc, featureidkey=f_id, z=dff[selected_metric],
    #     colorscale=METRICS[selected_metric]["colorscale"], marker_opacity=0.7
    # ))
    # fig_map.update_layout(
    #     map=dict(style="carto-positron", center={"lat": 28.3, "lon": 84.1}, zoom=6),
    #     margin={"r":0,"t":0,"l":0,"b":0}
    # )
    fig_map = go.Figure()

    fig_map.add_trace(go.Choroplethmap(
        geojson=PROV_GEO,
        locations=[f['properties']['adm1_name'] for f in PROV_GEO['features']],
        featureidkey="properties.adm1_name",
        z=[0] * len(PROV_GEO['features']),
        colorscale=[[0, '#f8f9fa'], [1, '#f8f9fa']], # Very light grey base
        showscale=False,
        marker_opacity=1,
        marker_line_width=0.5,
        marker_line_color="black",
        hoverinfo='skip'
        ))

    fig_map.add_trace(go.Choroplethmap(
        geojson=geo,
        locations=loc,
        featureidkey=f_id,
        z=dff[selected_metric],
        colorscale=METRICS[selected_metric]["colorscale"],
        marker_opacity=0.8,
        marker_line_width=1,
        marker_line_color="black",
        colorbar=dict(
            title=METRICS[selected_metric]["label"],
            thickness=15,
            len=0.5,
            x=0.9,
            y=0.5
        )
    ))

    fig_map.update_layout(
        map=dict(
            style="white-bg", 
            center={"lat": 28.3, "lon": 84.1}, 
            zoom=6
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)', 
    )

    table = dash_table.DataTable(
        data=dff.to_dict('records'),
        columns=[{"name": i.replace("_", " ").title(), "id": i} for i in dff.columns],
        page_size=8,
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': '#003893', 'color': 'white', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'left', 'padding': '10px'}
    )

    fig_bar = px.bar(
        dff.sort_values(selected_metric), 
        x=selected_metric, 
        y=dff.columns[0], 
        orientation='h',
        color=selected_metric,
        color_continuous_scale=METRICS[selected_metric]["colorscale"]
    )
    fig_bar.update_layout(margin={"r":10,"t":10,"l":10,"b":10}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    if view_level == "province":
        back_btn = html.Button(id={"type": "back-btn", "index": "main"}, style={"display": "none"})
    else:
        back_btn = html.Button(
            "← Back to Provinces", 
            id={"type": "back-btn", "index": "main"}, 
            className="btn btn-outline-danger w-100"
        )
    
    return fig_map, table, fig_bar, back_btn, {'level': view_level, 'filter': target_filter}
