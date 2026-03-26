from dash import Dash
import dash_bootstrap_components as dbc

FA = "https://use.fontawesome.com/releases/v5.15.4/css/all.css"

dash_app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
dash_app.config.suppress_callback_exceptions = True

server = dash_app.server