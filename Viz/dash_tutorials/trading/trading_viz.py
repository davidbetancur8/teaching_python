# ===================================================================
# Importante tener el stylesheet.css dentro de el directorio assets
# ===================================================================

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import yfinance as yf
from dash.dependencies import Output, Input, State

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
    html.Div([
        html.H2(children="Stocks"),
        html.Img(src="assets/336.jpg")
        ],
        className = "banner"
    ),
    html.Div([
        dcc.Input(
            id = "stock_input",
            placeholder = "Enter a stock to be charted",
            type = "text",
            value = "AAPL"
        ),
        dbc.Button(
            id="submit-button",
            n_clicks=0,
            children="submit"
        )
    ]),

    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id = "close_chart",
                )
            )
            
        ),

        dbc.Col([
            html.Div(
                dcc.Graph(
                    id = "high_chart",
                )
            )
            

        ]),

    ])

])



@app.callback(Output("close_chart", "figure"),
            [Input("submit-button", "n_clicks")],
            [State("stock_input", "value")])

def update_fig(n_clicks, input_value):
    df = yf.download(input_value, start, end)
    data = []
    trace_close = go.Scatter(
        x = df.index,
        y = df.Close,
        name = "High",
        line={
            "color": "#f44242"
        }
    )
    data.append(trace_close)
    return {
        "data": data
    }

if __name__ == "__main__":
    app.run_server(port=4050)
