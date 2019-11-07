import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import pandas as pd

### Functional World Map and Slider###
#SUCCESS

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
df = df[df.Country != "World"]
country_list = list(df["Country"].value_counts().sort_index().index)
year_list = list(df["Year"].value_counts().sort_index().index)
date_list = [str(each_year) for each_year in range(1900, 2018)]
date_mark = {int(date_list[i]): date_list[i] for i in range(0, len(date_list), 10)}

########### Initiate the app
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

########### Create Figure
"""World Chloropleth Map"""

def getFig(value):
    fig = go.Figure(
        data=go.Choropleth(
            locations=df.loc[df["Year"] == value]["Country Code"],
            z=df.loc[df["Year"] == value]["Annual_CO2_Emissions"],
            text=df.loc[df["Year"] == value]["Country"],
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
        geo=dict(
            showframe=False, showcoastlines=False, projection_type="equirectangular"
        ),
        annotations=[
            dict(
                x=0.55,
                y=0.1,
                xref="paper",
                yref="paper",
            )
        ],
    )

    return fig

############ Create Layout
"""Drop Down"""

app.layout = html.Div(
    [
        html.H5("Select a Year"),
        dcc.Slider(
            id="year-slider",
            min=int(date_list[0]),
            max=int(date_list[-1]),
            step=1,
            marks=date_mark,
            value=2010,
        ),
        html.Br(),
        dcc.Graph(id="world-map"),
        html.A("Code on Github", href=githublink),
        html.Br(),
        html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output("world-map", "figure"), [Input("year-slider", "value")])
def updateFigWith(value):
    return getFig(value)

############ Deploy
if __name__ == "__main__":
    app.run_server(debug=True)
