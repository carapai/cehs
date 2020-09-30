from components import (
    country_overview_scatter,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
)
from dash.dependencies import Input, Output, State
from store import (
    define_datasets,
    dfs,
    district_control_group,
    indicator_dropdown_group,
    init_data_set,
    outlier_policy_dropdown_group,
    reference_date,
    static,
    target_date,
)

from .global_callbacks import change_titles, global_story_callback, update_on_click
from .user_interface import (
    change_page,
    download_data,
    toggle_fade_controls,
    toggle_fade_info,
)

callback_ids = {
    outlier_policy_dropdown_group.dropdown_ids[-1]: "value",
    indicator_dropdown_group.dropdown_ids[-1]: "value",
    reference_date.dropdown_ids[0]: "value",
    reference_date.dropdown_ids[-1]: "value",
    target_date.dropdown_ids[0]: "value",
    target_date.dropdown_ids[-1]: "value",
    district_control_group.dropdown_ids[-1]: "value",
    indicator_dropdown_group.dropdown_ids[0]: "value",
    indicator_dropdown_group.dropdown_ids[1]: "value"
}


def define_callbacks(ds):

    app = ds.app

    callbacks = [
        # Global callbacks
        {
            "inputs": [Input(x, y) for (x, y) in callback_ids.items()],
            "outputs": [Output("ds-container", "children")],
            "function": global_story_callback,
        },
        {
            "inputs": [Input(x, y) for (x, y) in callback_ids.items()],
            "outputs": [
                Output(f"{country_overview_scatter.my_name}_title", "children"),
                Output(f"{district_overview_scatter.my_name}_title", "children"),
                # Output(f"{stacked_bar_reporting_country.my_name}_title", "children"),
                Output(f"{tree_map_district.my_name}_title", "children"),
            ],
            "function": change_titles,
        },
        {
            "inputs": [Input(f"{tree_map_district.my_name}_figure", "clickData")],
            "outputs": [
                Output(f"{facility_scatter.my_name}_figure", "figure"),
                Output(f"{facility_scatter.my_name}_fig_title", "children"),
            ],
            "function": update_on_click,
        },
        # User interface
        {
            "inputs": [Input("fade-button", "n_clicks")],
            "outputs": [Output("fade", "is_in")],
            "function": toggle_fade_controls,
            "states": [State("fade", "is_in")],
        },
        {
            "inputs": [Input("fade-button2", "n_clicks")],
            "outputs": [Output("fade2", "is_in")],
            "function": toggle_fade_info,
            "states": [State("fade2", "is_in")],
        },
        {
            "inputs": [Input("download-excel", "n_clicks")],
            "outputs": [Output("download-excel", "href")],
            "function": download_data,
        },
        {
            "inputs": [
                Input("dashboard-button", "n_clicks"),
                Input("reporting-button", "n_clicks"),
                Input("overview-button", "n_clicks"),
            ],
            "outputs": [
                Output("ds-paginator", "children"),
                Output("paginator", "children"),
            ],
            "function": change_page,
        },
    ]

    # {
    #         "inputs": ,
    #         "outputs": ,
    #         "function": ,
    # },

    for callback in callbacks:
        app.callback(
            output=callback.get("outputs", []),
            inputs=callback.get("inputs", []),
            state=callback.get("states", []),
        )(callback.get("function"))
