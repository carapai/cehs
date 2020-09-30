from dash import callback_context
from store import download_file, dfs
from view import ds, paginator
from components import (
    country_overview_scatter,
    country_overview,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
    reporting_map,
    grid,
    statistics,
)


def toggle_fade_controls(n, is_in):
    if not n:
        # Button has never been clicked
        is_in = True
    out = not is_in
    return [out]


def toggle_fade_info(n, is_in):
    if not n:
        # Button has never been clickedppy
        is_in = True
    out2 = not is_in
    return [out2]


def download_data(n_clicks):
    if n_clicks:
        print("Yes")
        href_data = download_file(dfs)

        return [href_data]
    else:
        return [None]


def change_page(*inputs):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    if "dashboard-button" in changed_id:
        ds.data_cards = [
            country_overview_scatter,
            country_overview,
            district_overview_scatter,
            tree_map_district,
            facility_scatter,
        ]
        paginator.clicked = "Dashboard"
    elif "reporting-button" in changed_id:
        ds.data_cards = [
            stacked_bar_reporting_country,
            reporting_map,
            stacked_bar_district,
        ]
        paginator.clicked = "Reporting"
    elif "overview-button" in changed_id:
        ds.data_cards = [statistics, grid]
        paginator.clicked = "Overview"

    return [ds.get_container(), paginator.get_layout()]
