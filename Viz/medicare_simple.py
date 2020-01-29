# Ejemplo para un scatterplot muy simple con dash usando el dataset de medicare

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("data/medicare.csv")


df_grouped = df.groupby(["brand_name"])["total_spending", "beneficiary_count"].mean()

app.layout = html.Div([
    dcc.Graph(
        id='spendings-vs-beneficiaries',
        figure={
            'data': [
                dict(x = df_grouped.total_spending, 
                     y = df_grouped.beneficiary_count,
                     name=df.index,
                     text=df.brand_name,
                     mode="markers", # marker para lineas y markers para puntos
                     marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    })
            ],
            'layout': dict(
                title="Expendings in medical care USA",
                xaxis={'type': 'log', 'title': 'total_spending'},
                yaxis={'title': 'beneficiary_count'},
                margin={'l': 80, 'b': 40, 't': 40, 'r': 80},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)