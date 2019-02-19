import datetime
import pandas_datareader.data as web
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas_datareader as pdr
import pandas as pd

import plotly.graph_objs as go


start_year = 2015
start_month = 1
start_day = 1

start = datetime.datetime(start_year, start_month, start_day)
end = datetime.datetime.now()

## WE make a list of all the data tables we need for our dashboard info
list_ur = [ "ALURN", "AKURN", "AZURN", "ARURN", "CAURN", "COURN", "CTURN", "DEURN", "FLURN",
    "GAURN", "HIURN", "IDURN", "ILURN", "INURN", "IAURN", "KSURN", "KYURN", "LAURN", "MEURN", "MDURN", "MAURN",
    "MIURN", "MNURN", "MSURN", "MOURN", "MTURN", "NEURN", "NVURN", "NHURN", "NJURN", "NMURN", "NYURN", "NCURN", "NDURN",
    "OHURN", "OKURN", "ORURN", "PAURN", "RIURN", "SCURN", "SDURN", "TNURN", "TXURN", "UTURN", "VTURN", "VAURN", "WAURN",
    "WVURN", "WIURN", "WYURN"]

list_pop = [ "ALPOP", "AKPOP", "AZPOP", "ARPOP", "CAPOP", "COPOP", "CTPOP", "DEPOP", "FLPOP",
    "GAPOP", "HIPOP", "IDPOP", "ILPOP", "INPOP", "IAPOP", "KSPOP", "KYPOP", "LAPOP", "MEPOP", "MDPOP", "MAPOP",
    "MIPOP", "MNPOP", "MSPOP", "MOPOP", "MTPOP", "NEPOP", "NVPOP", "NHPOP", "NJPOP", "NMPOP", "NYPOP", "NCPOP", "NDPOP",
    "OHPOP", "OKPOP", "ORPOP", "PAPOP", "RIPOP", "SCPOP", "SDPOP", "TNPOP", "TXPOP", "UTPOP", "VTPOP", "VAPOP", "WAPOP",
    "WVPOP", "WIPOP", "WYPOP"]

df = web.DataReader("TXURN", 'fred', start, end)

#print(df.head())

count = 0
for item in list_ur :
    #print(item)
    if count == 0:
        df = web.DataReader(item,'fred', start, end)
        count = count+1
        #print(df.head())
    else :
        df_temp = web.DataReader(item, "fred", start, end)
        df = pd.merge(df, df_temp, on = "DATE")
        #print(df.head())

#print(df.head())
count = 0
for item in list_pop:
    if count == 0:
        db = web.DataReader(item, "fred", start, end)
        #print(db)
        count = count+1
    else:
        db_temp = web.DataReader(item, "fred", start, end)
        db = pd.merge(db, db_temp, on="DATE")
        count = count + 1
#print(db)

### THIS IS THE DATA WE NEED TO PLOT
#print(df.loc[df.index=="2015-01-01"])



app = dash.Dash()


app.layout = html.Div([
    html.Label('Choose Date :'),
    dcc.Dropdown(
        id = "input",
        options=[
            {'label': '2015', 'value': '2015-01-01'},
            {'label': '2016', 'value': '2016-01-01'},
            {'label': '2017', 'value': '2017-01-01'},
            {'label': '2018', "value": '2018-01-01'}
        ],
        value='2015-01-01'
    ),
    html.Div(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)


###PAS ENCORE FINI CA
def update_value(input_data):


    return dcc.Graph(
        id="output-graph",
        figure={
            'data': [
                go.Scatter(
                    x=(db.loc[db.index==input_data].astype(str) == i)['population in state'],
                    y= (df.loc[df.index==input_data].astype(str) == i)['unemployment rate in state'],
                    #text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.index.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'POP'},
                yaxis={'title': 'unemployment'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True),
    #app.config['suppress_callback_exceptions']=True
