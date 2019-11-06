import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import pandas as pd

### Functional World Map and Slider Attempt 1 ###

########### Define the data

tabtitle = "CO2 Emissions"
sourceurl = "http://www.globalcarbonatlas.org/en/CO2-emissions"
githublink = "https://github.com/ktemsupa/final-project"
capita = pd.read_csv(
    "/Users/KimberlyElise/General_Assembly/newproject/final-project/data/emissions_capita.csv"
)
region = pd.read_csv(
    "/Users/KimberlyElise/General_Assembly/newproject/final-project/data/emissions_region.csv"
)
# Merge dataset
df = pd.merge(capita, region)
# Create range of years for x-axis
df = df[df["Year"].between(1900, 2017)]
# Rename columns
df.rename(
    columns={
        "Entity": "Country",
        "Code": "Country Code",
        "Annual CO₂ emissions (tonnes )": "Annual_CO2_Emissions",
        "Per capita CO₂ emissions (tonnes per capita)": "Per_Capita_CO2_Emissions",
    },
    inplace=True,
)
country_list = list(df["Country"].value_counts().sort_index().index)
year_list = list(df["Year"].value_counts().sort_index().index)

########### Initiate the app
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

########### Create Figure
'''World Chloropleth Map'''

def getFig(value):
    fig = go.Figure(
        data=go.Choropleth(
            locations=df["Country Code"],
            z=df["Annual_CO2_Emissions"],
            text=df["Country"],
            colorscale="RdYlBu",
            autocolorscale=False,
            reversescale=True,
            marker_line_color="darkgray",
            marker_line_width=0.5,
            colorbar_tickprefix="-",
            colorbar_title="CO2 Emissions<br>(tonnes)",
        )
    )

    fig.update_layout(
        title_text="Annual CO2 Emissions",
        geo=dict(showframe=False, showcoastlines=False, projection_type="equirectangular"),
        annotations=[
            dict(
                x=0.55,
                y=0.1,
                xref="paper",
                yref="paper",
                text='Source: <a href="http://www.globalcarbonatlas.org/en/CO2-emissions">\
                Global Carbon Atlas</a>',
                showarrow=False,
            )
        ],
    )

    return fig

############ Create Layout

date_list = ['1900', '1920', '194', '2013', '2014', '2015', '2016', '2017']
date_mark = {i: date_list[i] for i in range (0,8)}


# Dropdown
app.layout = html.Div([
    html.H3('Select a Year'),
    dcc.RangeSlider(
        id='year-slider',
        min = 0,
        max = 7,
        step = None,
        #marks = [{'label': i, 'value': i} for i in year_list],
        marks = date_mark,
        value = [3, 4]
    ),
    html.Br(),
    dcc.Graph(id='world-map'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


############ Callbacks

@app.callback(Output('world-map', 'figure'),
             [Input('year-slider', 'value')])
def updateFigWith(value):
    return getFig(value)


############ Deploy
if __name__ == "__main__":
    app.run_server(debug=True)
