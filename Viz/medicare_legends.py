import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("data/medicare.csv")
df["year_str"] = df["year"].astype("str")
df["year_brand"] = df[['year_str', 'brand_name']].apply(lambda x: ''.join(x), axis=1)


app.layout = html.Div([
    dcc.Graph(
        id='spendings-vs-beneficiaries',
        figure={
            'data': [
                dict(
                    x=df[df['brand_name'] == i]['total_spending'],
                    y=df[df['brand_name'] == i]['beneficiary_count'],
                    text=df[df['brand_name'] == i]['year_brand'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.brand_name.unique()
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