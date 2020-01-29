# https://data.world/carlvlewis/medicare-rx-spending-10-15

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Configuración
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# DataFrame
df = pd.read_csv("data/medicare.csv")

# App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     [Input('year-slider', 'value')])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#     traces = []
#     for i in filtered_df.brand_name.unique():
#         df_by_continent = filtered_df[filtered_df['brand_name'] == i]
#         traces.append(dict(
#             x=df_by_continent['total_spending'],
#             y=df_by_continent['beneficiary_count'],
#             text=df_by_continent['brand_name'],
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name=i
#         ))

#     return {
#         'data': traces,
#         'layout': dict(
#             xaxis={'type': 'log', 'title': 'GDP Per Capita',
#                    'range':[2.3, 4.8]},
#             yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest',
#             transition = {'duration': 500},
#         )
#     }


if __name__ == '__main__':
    app.run_server(debug=True)