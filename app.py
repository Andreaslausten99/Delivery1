# ***************************************
# Imports
# ***************************************
# Dash
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Div.
import pandas as pd
import numpy as np
import calendar

# Plotly
import plotly.express as px
import plotly.graph_objects as go

# ***************************************
# Get data
# ***************************************
import datamodel
order = datamodel.get_data()
df_year = datamodel.get_year()
df_month = datamodel.get_month()


# ***************************************
# Diagram - Employee Sales
# ***************************************
def employesssale():
    fig = px.scatter(order, x='employee_id', y='order_id', title='Sales by employee')
    return fig    

def categorysale():
    fig = px.scatter(order, x='product_id', y='order_id', title='Sales by products')
    return fig

# ***************************************
# Activate the app
# ***************************************
#app = dash.Dash(__name__)

app = dash.Dash()

app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)

body_app = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = 'employee_id', figure=employesssale()),
            style = {'height':'400px'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6),
        dbc.Col(
            dcc.Graph(id = 'product_id', figure=categorysale()),
            style = {'height':'400px'},xs = 12, sm = 12, md = 6, lg = 6, xl = 6),
    ]),

],fluid = True) 

topbar = dbc.Navbar(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavbarBrand("Delivery 1 - 28-03-2022", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
                    ),
                )
            ],
            align="center",
            className="g-10",
        ),
    ]
)

dash_app = dash.Dash(__name__)
app = dash_app.server

# ***************************************
# Layout
# ***************************************

# ***************************************
# Callbacks
# ***************************************
# Output er diagrammet
# Input er DropDown
@dash_app.callback(Output('sales_employee', 'figure'),
              [Input('drop_month', 'value')],
              [Input('drop_year', 'value')])

def update_graph(drop_month, drop_year):
    if drop_year:
        if drop_month:
            # Data i både drop_month og drop_year
            order_fig1 = order.loc[(order['orderyear'] == drop_year) & (order['ordermonth'] == drop_month)]
        else:
            # Data i drop_year. men ikke drop_month
            order_fig1 = order.loc[order['orderyear'] == drop_year]
    else:
        if drop_month:
            # Data i drop_month, men ikke drop_year
            order_fig1 = order.loc[order['ordermonth'] == drop_month]
        else:
            # Ingen data - ikke noget valgt
            order_fig1 = order
        
    return {'data':[go.Bar(
        x = order_fig1['productname'],
        y = order_fig1['total']
            )
        ]
    }

# ***************************************
# Run the app
# ***************************************
if __name__ == '__main__':
    dash_app.run_server(debug=True)
