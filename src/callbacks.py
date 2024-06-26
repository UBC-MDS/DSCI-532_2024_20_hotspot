from dash import Input, Output, callback
import src.hotspot_plot as hp
from src.data import df
from flask_caching import Cache

TIMEOUT = 1800  # 30 minutes

# Initialize cache
cache = Cache()


# Controls for Interactive Plot
@callback(
    Output("world-map", "figure"),
    Output("global-temp-co2", "spec"),
    Output("total-co2", "children"),
    Output("fun-fact", "children"),
    Output("year-header", "children"),
    Input("year-slider", "value"),
    Input("country-dropdown", "value"),
)
@cache.memoize(timeout=TIMEOUT)
def update_(year, country):
    """
    Update all the plots based on the year range and selected countries.
    This is only when country is changed from the dropdown.
    """

    df_filtered = hp.filter_data(df, country, start_year=year[0], end_year=year[1])

    world_map_fig = hp.plot_world_map(df_filtered)
    global_temp_co2_fig = hp.plot_global_temp_co2(
        df_filtered, start_year=year[0], end_year=year[1]
    )
    top_emitters_fig = hp.plot_top_emitters(df_filtered)
    top_emitters_per_capita_fig = hp.plot_top_emitters_per_capita(df_filtered)

    total_co2 = hp.get_total_co2_emissions(df_filtered)
    total_co2_fig = f"{total_co2:,.0f} GT"
    num_empire_state_buildings = hp.get_number_of_esb(total_co2)
    fun_fact_fig = f"This is equivalent to {num_empire_state_buildings:,} Empire State Buildings in volume!"

    year_header = f"Over selected countries and year range: {year[0]} - {year[1]}"

    # Return the data
    return (
        world_map_fig,
        global_temp_co2_fig,
        total_co2_fig,
        fun_fact_fig,
        year_header,
    )


@callback(
    Output("co2-emissions-ranking", "spec"),
    Input("total-per-capita-button", "value"),
    Input("year-slider", "value"),
    Input("country-dropdown", "value"),
)
@cache.memoize(timeout=TIMEOUT)
def update_emission_graphs(tab, year, country):
    df_filtered = hp.filter_data(df, country, start_year=year[0], end_year=year[1])

    if tab == "tab-total":
        co2_rank_fig = hp.plot_top_emitters(df_filtered)
    elif tab == "tab-per-capita":
        co2_rank_fig = hp.plot_top_emitters_per_capita(df_filtered)

    return co2_rank_fig


@callback(
    Output("country-dropdown", "value"),
    Input("world-map", "selectedData"),
)
def update_dropdown(map_selected_data):
    """
    Update the country dropdown based on the selected countries on the map.
    """
    if map_selected_data:
        selected_countries = set(
            point["location"] for point in map_selected_data["points"]
        )
        country_dropdown_value = list(selected_countries)
        return country_dropdown_value
    return []
