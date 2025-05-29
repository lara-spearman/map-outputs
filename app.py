from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd

layer_info = {
    # "Sustrans National Cycle Network Route":{"group":"Map5",
    #                                         "group_field":"None"},
    # "Sustrans_Regional Cycle Route":{"group":"Map5",
    #                  "group_field":"None"},
    # "Sustrans Reclassified Cycle Route":{"group":"Map5",
    #                  "group_field":"None"},
    # "Public Rights of Way":{"group":"Map5",
    #                  "group_field":"LYR_NAME"},
    # "FC Forest Roads":{"group":"Map5",
    #                  "group_field":"None"},
    # "CRoW S16 Dedicated Land":{"group":"Map5",
    #                  "group_field":"None"},
    # "CRoW_S15 Land All Types":{"group":"Map5",
    #                  "group_field":"None"},
    # "Conclusive Registered Commons":{"group":"Map5",
    #                  "group_field":"None"},
    # "Conclusive Open Country":{"group":"Map5",
    #                  "group_field":"None"},
    #  "CRoW Access Land":{"group":"Map5",
    #                  "group_field":"None"},
    # "OS Greenspace":{"group":"Map5",
    #                  "group_field":"function"},
    # "NE Country Parks":{"group":"Map5",
    #                  "group_field":"None"},
    # "Agricultural Land Classification":{"group":"Map6",
    #                  "group_field":":ALC_GRADE"},
    # "Environmental Stewardship Scheme":{"group":"Map7",
    #                  "group_field":"SCHEME"},
    "Organic Farming Scheme":{"group":"Map7",
                     "group_field":"SCHEME"},
    # "Countryside Stewardship Scheme":{"group":"Map7",
    #                  "group_field":"CS_TYPE"},
    "RPA Landcovers":{"group":"Map8",
                     "group_field":"COVER_TYPE"},
    # "RPA Land Parcels":{"group":"Map9",
    #                  "group_field":"FarmID"},
    # "WSBRC Wiltshire eNGO Sites":{"group":"Map10",
    #                  "group_field":""},
    # "WSBRC Wiltshire eNGO Sites":{"group":"Map10",
    #                  "group_field":""},
    
}

# location_data = "O:/LocalAuthorities/Neighbourhood_Plans/Research/NeigbourhoodPlansPython"
# df_all = pd.DataFrame({'NAME': [], 'sum_Area_HECTARES': [],'groupColumnValue': [],'groupColumnName': [],'mapGroup': [],'mapName': []})
# # def create_dataframe():
    
# for layer in layer_info.keys():
#     layer_name = layer.replace(" ","_")
#     df_table = pd.read_csv(f"{location_data}/{layer_info[layer]['group']}_{layer_name}_table.csv")
#     df_layer = pd.read_csv(f"{location_data}/{layer_info[layer]['group']}_{layer_name}.csv")
#     df_table.rename(columns = {f"{layer_info[layer]['group_field']}":"groupColumnValue"}, inplace=True)
#     #df_table.rename(columns = {"sum_Area_HECTARES":"groupColumnValue"}, inplace=True)
#     df_layer_all = df_layer[["NAME", "Join_ID"]].merge(df_table, on="Join_ID")
#     df_layer_all = df_layer_all[['NAME', 'sum_Area_HECTARES',  
#     "groupColumnValue"]]
#     df_layer_all["mapGroup"] = f"{layer_info[layer]['group']}"
#     df_layer_all["mapName"] = f"{layer_name}"
#     df_layer_all["groupColumnName"] = layer_info[layer]['group_field']
#     #df_all = df_all.append(df_layer_all)
#     df_all = pd.concat([df_all,df_layer_all ])
#     # return df_all
# # df_all = create_dataframe()
# print(df_all)

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
                    dcc.Graph(id='graph-content'),
                    dash_table.DataTable(id = "table-content",sort_action='native'),
                ]),
        dcc.Tab(label = "PC drilldown", children = 
                [
                    html.H1(children='Analysis Parish Council', style={'textAlign':'center'}),
                    dcc.Dropdown(df_all.NAME.unique(), 'Colerne', id='dropdown-selection-pc'),
                    dcc.Dropdown(df_all.mapName.unique(), 'RPA_Landcovers', id='dropdown-selection-map-pc'),
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
    Input('dropdown-selection-variable', 'value')
)
def update_graph(value1, value2):

    df_filter = df_all[df_all.mapName==value1]
    dff = df_filter[df_filter.groupColumnValue==value2]
    x_axis_name = dff.unitName.unique()[0]
    #dff['value']=dff['value'].map("{:,.0f}".format)
    dff_sorted = dff.sort_values(by = "value", ascending= False)
    dff_sorted['value'] = dff_sorted['value'].round(1)
    fig = px.bar(dff_sorted, x='NAME', y='value', template = "simple_white", labels = {"value":x_axis_name})
    

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
    dff = df_filter[df_filter.mapName==value2]
    x_axis_name = dff.unitName.unique()[0]
    dff_sorted = dff.sort_values(by = "value", ascending= False)
    dff_sorted['value'] = dff_sorted['value'].round(1)
    fig = px.bar(dff_sorted, x='groupColumnValue', y='value', template = "simple_white", labels = {"value":x_axis_name, "groupColumnValue":"Type"})
    

    table_data_filtered = dff_sorted[['groupColumnValue', 'value', "unitName"]]
    table_data = table_data_filtered.to_dict('records')

    return fig, table_data#', columns_data

if __name__ == '__main__':
    app.run(debug=True)