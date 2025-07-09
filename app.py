from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


df_all = pd.read_csv('test.csv')

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label = "PC comparison", children = 
                [
                    html.H1(children='Analysis', style={'textAlign':'center'}),
                    dcc.Dropdown(df_all.mapName.unique(), 'RPA_Landcovers', id='dropdown-selection-dataset'),
                    dcc.Dropdown(value = 'Arable land', id='dropdown-selection-variable'),
                     dcc.Dropdown(df_all.NAME.unique(), value = 'Colerne', id='dropdown-selection-pc-comparison'),
                    dcc.Graph(id='graph-content'),
                    dash_table.DataTable(id = "table-content",sort_action='native'),
                ]),
        dcc.Tab(label = "PC drilldown", children = 
                [
                    html.H1(children='Analysis Parish Council', style={'textAlign':'center'}),
                    dcc.Dropdown(df_all.NAME.unique(), 'Colerne', id='dropdown-selection-pc'),
                    dcc.Dropdown(df_all.mapGroup.unique(), 'Map5', id='dropdown-selection-map-pc'),
                    dcc.Graph(id='graph-content-pc'),
                    dash_table.DataTable(id = "table-content-pc",sort_action='native'),
                ])
    ])
]
    
)

@callback(
    Output('dropdown-selection-variable', 'options'),
    Input('dropdown-selection-dataset', 'value'))
def set_column_options(selected_dataset):
    df_dataset = df_all[df_all.mapName == selected_dataset] 
    return df_dataset.groupColumnValue.unique()



@callback(
    Output('graph-content', 'figure'),
    Output('table-content', 'data'),    
    Input('dropdown-selection-dataset', 'value'),
    Input('dropdown-selection-variable', 'value'),
    Input('dropdown-selection-pc-comparison', 'value'),
)
def update_graph(value1, value2, value3):

    df_filter = df_all[df_all.mapName==value1]
    dff = df_filter[df_filter.groupColumnValue==value2]
    try:
        x_axis_name = dff.unitName.unique()[0]
    except:
        x_axis_name = ""
    #dff['value']=dff['value'].map("{:,.0f}".format)
    dff_sorted = dff.sort_values(by = "value", ascending= False)
    dff_sorted['value'] = dff_sorted['value'].round(1)
    dff_sorted['color'] = np.where(dff_sorted.NAME == value3,  '#e377c2', '#1f77b4')
    #fig = px.bar(dff_sorted, x='NAME', template = "simple_white", labels = {"value":x_axis_name})
    fig = go.Figure(data=[go.Bar(
    x=dff_sorted.NAME,
    y=dff_sorted.value,

    marker_color=dff_sorted['color'] 
    )])
    fig.update_layout(template= "simple_white")

    table_data_filtered = dff_sorted[['NAME', 'value','groupColumnValue', "unitName"]]
    #table_data_filtered['values'] = table_data_filtered['values'].round()
    table_data = table_data_filtered.to_dict('records')
    return fig, table_data


@callback(
    Output('graph-content-pc', 'figure'),
    Output('table-content-pc', 'data'),
    #Output('table-content-pc', 'columns'),
    Input('dropdown-selection-pc', 'value'),
    Input('dropdown-selection-map-pc', 'value')
)
def update_graph(value1, value2):

    df_filter = df_all[df_all.NAME==value1]
    dff = df_filter[df_filter.mapGroup==value2]
    try:
        x_axis_name = dff.unitName.unique()[0]
    except:
        x_axis_name = ""
    # x_axis_name = dff.unitName.unique()[0]
    dff_sorted = dff.sort_values(by = "value", ascending= False)
    dff_sorted['value'] = dff_sorted['value'].round(1)
    fig = px.bar(dff_sorted, x='groupColumnValue', y='value', template = "simple_white", labels = {"value":x_axis_name, "groupColumnValue":"Type"})
    

    table_data_filtered = dff_sorted[['groupColumnValue', 'value', "unitName"]]
    table_data = table_data_filtered.to_dict('records')

    return fig, table_data#', columns_data

if __name__ == '__main__':
    app.run(debug=True)