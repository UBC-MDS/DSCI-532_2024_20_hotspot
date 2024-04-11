from dash import Dash, html
import dash_bootstrap_components as dbc

import src.callbacks
from src.components import (
    title_header,
    page_footer,
    year_slider,
    country_dropdown,
    world_map,
    top_emitters,
    global_temp_co2,
    total_co2,
    fun_fact,
)

# Initialize Dash app
app = Dash(__name__, title="Hotspot", external_stylesheets=[dbc.themes.FLATLY])
server = app.server


# Define layout
app.layout = dbc.Container(
    [
        # HEADER
        html.Div(
            title_header,
            className="app-header",
        ),
        html.Hr(),
        dbc.Row(
            [
                # First container, contains widgets (year range, countries) & key KPI
                dbc.Col(
                    [
                        html.H4("Filter Options"),
                        html.H5("Select Year Range"),
                        year_slider,
                        html.H5("Select Countries"),
                        country_dropdown,
                        html.Br(),
                        html.H4("Total CO2 Emission:"),
                        total_co2,
                        html.P("Over selected countires and year range"),
                        html.Br(),
                        fun_fact,
                    ],
                    className="app-widget",
                ),
                # Second container, contains map (left), top CO2 emitters (top right), &
                # temperature vs CO2 over time (bottom right)
                dbc.Col(
                    [
                        html.H4("World Map of CO2 Emissions"),
                        world_map,
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4("Top CO2 Emitters"),
                                        top_emitters,
                                    ]
                                ),
                                dbc.Col(
                                    [
                                html.H4("Temperature and CO2 Emissions over Time"),
                                global_temp_co2,
                                    ]
                                ),                                
                            ]
                        )
                    ],
                    align="center",
                    md=9,
                ),
            ],
            className="app-row",
        ),
        html.Footer(
            page_footer,
            className="app-footer",
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True)  # Remember to change to False before deploying
