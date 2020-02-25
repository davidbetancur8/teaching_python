import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px



df = pd.read_csv("data/1000 Sales Records.csv")

# =================================================
# Profit por mes
# =================================================
df_profit = df.loc[:,["Order Date", "Item Type", "Total Profit"]]
df_profit['Order Date'] = pd.to_datetime(df_profit['Order Date'])
df_profit['YearMonth'] = df_profit['Order Date'].apply(lambda x: '{year}-{month}'.format(year=x.year, month=x.month))
df_profit = df_profit.sort_values("YearMonth")
df_profit_month = df_profit.groupby(["YearMonth", "Item Type"]).sum().reset_index()
df_profit_month = df_profit_month.sort_values(["YearMonth", "Total Profit"], ascending = False)

def generate_figure_sales_mes():
    fig = px.bar(df_profit_month, 
             y="Total Profit", x="Item Type",
             title='Profit by items for month',
             animation_frame="YearMonth",
             color_discrete_sequence=["rgba(171, 152, 240, 0.66)"]
             )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    # fig.update_traces(marker_color='rgb(171, 152, 240)', marker_line_color='rgb(37, 7, 145)', 
    #                 marker_line_width=1.5, opacity=0.66)
    return fig
# =================================================


# =================================================
# Profit total
# =================================================
df_profit_total = df.loc[:,["Item Type", "Total Profit"]]
df_profit_total = df_profit_total.groupby("Item Type").sum().reset_index().sort_values("Total Profit", ascending = False)

def generate_figure_sales_total():
    fig = px.bar(df_profit_total, 
             y="Total Profit", x="Item Type",
             title='Number of Cases outside China', color='Total Profit')

    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.6)
    return fig

# =================================================


# =================================================
# Profit by country each month
# =================================================
df_profit_country = df.loc[:,["Order Date", "Country", "Total Profit"]]
df_profit_country['Order Date'] = pd.to_datetime(df_profit_country['Order Date'])
df_profit_country['YearMonth'] = df_profit_country['Order Date'].apply(lambda x: '{year}-{month}'.format(year=x.year, month=x.month))

def generate_figure_sales_mes_world():
    fig = px.scatter_geo(df_profit_country, locations="Country", locationmode='country names', 
                        color="Total Profit", size='Total Profit', hover_name="Country", range_color= [0, max(df_profit_country['Total Profit'])+2], 
                        projection="natural earth", animation_frame="YearMonth", title='Spread outside China over time')
    fig.update(layout_coloraxis_showscale=False)

    return fig

# =================================================


# =================================================
# delay by order day of week
# =================================================
df_dates = df.loc[:,["Order Date", "Ship Date", "Country"]]
df_dates["Order Date"] = pd.to_datetime(df_dates["Order Date"])
df_dates["Ship Date"] = pd.to_datetime(df_dates["Ship Date"])
df_dates["delay"] = df_dates['Ship Date'] - df_dates['Order Date']
df_dates["delay"] = df_dates["delay"].dt.days
df_dates["order_day"] = df_dates["Order Date"].dt.day_name()

df_dates_delay = df_dates.groupby("order_day")["order_day", "delay"].mean().reset_index()
cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_dates_delay['order_day'] = pd.Categorical(df_dates_delay['order_day'], categories=cats, ordered=True)
df_dates_delay = df_dates_delay.sort_values('order_day')

def generate_figure_delay_dow():
    fig = px.bar(df_dates_delay, 
                x="delay", y="order_day",
                title='Number of Cases outside China', color='delay',
                orientation="h")
    fig.update_traces(marker_color='rgb(171, 152, 240)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.6)

    return fig

# =================================================


# =================================================
# prioridad
# =================================================
df_priority = df["Order Priority"]
df_prioridad = pd.DataFrame(df_priority.value_counts()).reset_index().rename(columns={"index":"priority", "Order Priority":"cuenta"})

def generate_figure_priority():
    fig = px.pie(df_prioridad, 
                values='cuenta', 
                names='priority', 
                title='Population of European continent',
                color_discrete_sequence=px.colors.sequential.Burg)
    return fig

# =================================================

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Div([
        html.H2(children="Sales"),
        ],

    ),

    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id = "sales_mes",          
                    figure = generate_figure_sales_mes()
                )
            ),
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id = "sales_total",
                    figure = generate_figure_sales_total()
                )
            ),
            

        ),
        

    ]),

        dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(
                    id = "mapa_sales_month",
                    figure = generate_figure_sales_mes_world()

                )
            )
        ),
    ]),


    dbc.Row([
        dbc.Col([
            dcc.Graph(id = "time_series_profit"),
            dbc.RadioItems( 
                id="radio_mapa",
                    options = [
                        {'label': 'Dia', 'value': "d"},
                        {'label': 'Semana', 'value': "w"},
                        {'label': 'Mes', 'value': "m"},
                        {'label': 'Año', 'value': "y"}
                    ],
                    value = "m",
                    inline=True
            ),
            
        ]),

        dbc.Col(dcc.Graph(id = "delay_dow",figure = generate_figure_delay_dow()))
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id = "pie_chart_priority", figure = generate_figure_priority())
            )
        )
    ])




])

@app.callback(Output("time_series_profit", "figure"),
            [Input('radio_mapa', 'value')])

def update_time_series_profit(input_value):
    df_profit_series = df.loc[:,["Order Date", "Total Profit"]]
    df_profit_series["Order Date"] = pd.to_datetime(df_profit_series["Order Date"])
    df_profit_series = df_profit_series.set_index("Order Date")
    df_profit_sum_day = df_profit_series.groupby(pd.Grouper(freq=input_value)).sum().reset_index()

    fig = px.line(df_profit_sum_day, x="Order Date", y="Total Profit", hover_name="Order Date", render_mode="svg")  
    return fig


if __name__ == "__main__":
    app.run_server(port=4050)