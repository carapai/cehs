import os
from datetime import datetime

import dash
import dash_auth
import dash_core_components as dcc
import geopandas as gpd
import pandas as pd
from dash.dependencies import Input, Output, State
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine

from define_datasets import define_datasets
from dropdown import initiate_dropdowns
from helpers import month_order
from model import CardLayout, Datadownload, Methodology, Paginator
from package.components.methodology_section import MethodologySection
from package.components.nested_dropdown_group import NestedDropdownGroup
from package.layout.area_card import AreaDataCard
from package.layout.chart_card import ChartDataCard
from package.layout.data_story import DataStory
from package.layout.map_card import MapDataCard
from read_data import read_data
from static_info import download_file, meth_data

from components.datacard_1 import scatter_country_plot
from components.datacard_2 import bar_country_dated_plot, map_country_dated_plot
from components.datacard_3 import scatter_district_plot
from components.datacard_4 import scatter_facility_plot, tree_map_district_dated_plot
from components.datacard_5 import bar_reporting_country_plot
from components.datacard_6 import map_reporting_dated_plot
from components.datacard_7 import scatter_reporting_district_plot

# data

# Get set of credentials

load_dotenv(find_dotenv())

credentials = {}

for x in os.environ:
    if "DASH_AUTH" in x:
        login = x.split("DASH_AUTH_")[1]
        password = os.environ.get(x, os.environ.get("SECRET"))
        credentials[login] = password


shapefile = gpd.read_file("./coc-dashboard/data/shapefiles/shapefile.shp")

DATABASE_URI = os.environ["HEROKU_POSTGRESQL_CYAN_URL"]
engine = create_engine(DATABASE_URI)

# Pop data
# TODO Have those paths defined ina  better place than in teh code

pop = pd.read_csv(
    "./coc-dashboard/data/pop.csv",
    header=None,
    names=["district", "year", "male", "female", "total", "age"],
    dtype={
        "district": str,
        "year": int,
        "male": int,
        "female": int,
        "total": int,
        "age": str,
    },
)
pop_tgt = pd.read_csv(
    "./coc-dashboard/data/target_pop.csv",
    dtype={"indicator": str, "ages": str, "sex": str},
)


columns, data_reporting, data_outliers, data_std, data_iqr, indicator_group = read_data(
    engine, test=False
)


# Cronjob data

date_df = pd.read_csv("./coc-dashboard/data/chron_date.csv")
date_df["Date"] = pd.to_datetime(date_df.Date).dt.strftime("%B-%d-%Y")

# Build data dictionnaries

dfs = {
    "Correct outliers - using standard deviation": data_std,
    "Correct outliers - using interquartile range": data_iqr,
    "Keep outliers": data_outliers,
    "Reporting": data_reporting,
}

static = {"population data": pop, "target population type": pop_tgt}

for key, df in dfs.items():
    df["date"] = pd.to_datetime(df.date, errors="coerce")
    df = df.rename(columns=columns)
    dfs[key] = df

if os.path.isfile('./coc-dashboard/assets/cehs.xlsx') == False:
    download_file(dfs) # write to excel file for download

# Get content from the methodology file

# TODO find a better format for this than the .py file I have now

download_button = Datadownload()

meth_date = date_df["Date"].iloc[-1]

methodology_layout = MethodologySection(title="Methodology", data=meth_data(meth_date))
methodology = Methodology([methodology_layout])


# global init_data_set

(
    side_nav,
    outlier_policy_dropdown_group,
    indicator_dropdown_group,
    reference_date,
    target_date,
    district_control_group,
) = initiate_dropdowns(data_outliers, indicator_group)

CONTROLS = dict(
    outlier=outlier_policy_dropdown_group.dropdown_objects[0].value,
    indicator=indicator_dropdown_group.dropdown_objects[2].value,
    indicator_type=indicator_dropdown_group.dropdown_objects[0].value,
    district=district_control_group.dropdown_objects[0].value,
    target_year=target_date.dropdown_objects[0].value,
    target_month=target_date.dropdown_objects[1].value,
    reference_year=reference_date.dropdown_objects[0].value,
    reference_month=reference_date.dropdown_objects[1].value,
)

init_data_set = define_datasets(static=static, dfs=dfs, **CONTROLS)


########################################
#              DATACARDS               #
########################################


# DATACARD 1 #


country_overview_scatter = ChartDataCard(
    title="Overview: Across the country, the number of $label$ changed by between 04-2019 and 04-2020",
    fig_title="Total number of $label$ across the country",
    data=init_data_set,
    data_transform=scatter_country_plot,
    fig_type="Scatter",
)

country_overview_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        }
    }
)


# DATACARD 2 #


country_overview_map = MapDataCard(
    data=init_data_set,
    data_transform=map_country_dated_plot,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
)

bar_chart_ranks_bottom = ChartDataCard(
    data=init_data_set,
    data_transform=bar_country_dated_plot,
    fig_object="Bar",
    bar_mode="overlay",
)

country_overview = CardLayout(
    title="Percentage change in number of children under one receiving their $label$ between target and reference date",
    elements=[country_overview_map, bar_chart_ranks_bottom],
)

# TODO Define common color scale for map and barchart


# DATACARD 3 #


district_overview_scatter = ChartDataCard(
    title="Deep-dive in the selected district: The number of $label$ changed by % between 05-2019 and 05-2020",
    fig_title="Total number of $label$ in the selected district",
    data=init_data_set,
    data_transform=scatter_district_plot,
    fig_type="Scatter",
)

district_overview_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        }
    }
)


# DATACARD 4 #


tree_map_district = AreaDataCard(
    title="The contribution of individual facilities in the selected district",
    data=init_data_set,
    data_transform=tree_map_district_dated_plot,
    fig_object="Treemap",
)
tree_map_district.set_colors({"fig": ["#e2d5d1", "#96c0e0", "#3c6792"]})


facility_scatter = ChartDataCard(
    fig_title="Evolution of $label$ (click on the graph above to filter)",
    data=init_data_set,
    data_transform=scatter_facility_plot,
)

facility_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        }
    }
)


# DATACARD 5 #


stacked_bar_reporting_country = ChartDataCard(
    title="Reporting: On 05-2020, around % of facilities reported on their 105:1 form, and, out of these % reported for this $label$",
    data=init_data_set,
    data_transform=bar_reporting_country_plot,
    fig_title="Total number of facilities reporting on their 105:1 form and reported a positive number of $label$ in country",
    fig_object="Bar",
)

stacked_bar_reporting_country.set_colors(
    {"fig": ["rgb(42, 87, 131)", "rgb(247, 190, 178)", "rgb(211, 41, 61)"]}
)

# DATACARD 6 #


reporting_map = MapDataCard(
    data=init_data_set,
    data_transform=map_reporting_dated_plot,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
)

# DATACARD 7 #


stacked_bar_district = ChartDataCard(
    data=init_data_set,
    data_transform=scatter_reporting_district_plot,
    fig_title="Total number of facilities reporting on their 105:1 form and reporting on $label$",
    fig_object="Bar",  # Relies on the 'overlay' layout barmode parameter for stacking
)

stacked_bar_district.set_colors(
    {"fig": ["rgb(42, 87, 131)", "rgb(247, 190, 178)", "rgb(211, 41, 61)"]}
)


##############
#   LAYOUT   #
##############

paginator = Paginator()

ds = DataStory(
    data_cards=[
        country_overview_scatter,
        country_overview,
        district_overview_scatter,
        tree_map_district,
        facility_scatter,
    ],
    ind_elements=[side_nav, download_button, methodology, paginator],
    footer_image="/static/images/UNICEF-MOH-bottom-resized.jpg",
    title="Continuity of Essential Health Services",
    sub_title="Overview of country, district and health facility-level health services in Uganda",
    footer_text=dcc.Link(
        children="Dalberg Data Insights - Contact Us",
        href="mailto:ddi_support@dalberg.com",
    ),
)

app = ds.app
app.title = "CEHS Uganda"

auth = dash_auth.BasicAuth(app, credentials)

#################
#   CALLBACKS   #
#################


callback_ids = {
    outlier_policy_dropdown_group.dropdown_ids[-1]: "value",
    indicator_dropdown_group.dropdown_ids[-1]: "value",
    reference_date.dropdown_ids[0]: "value",
    reference_date.dropdown_ids[-1]: "value",
    target_date.dropdown_ids[0]: "value",
    target_date.dropdown_ids[-1]: "value",
    district_control_group.dropdown_ids[-1]: "value",
    indicator_dropdown_group.dropdown_ids[0]: "value",
}


@app.callback(
    [Output("ds-container", "children")],
    [Input(x, y) for (x, y) in callback_ids.items()],
)
def global_story_callback(*inputs):

    outlier = inputs[0]
    indicator = inputs[1]
    reference_year = inputs[2]
    reference_month = inputs[3]
    target_year = inputs[4]
    target_month = inputs[5]
    district = inputs[6]
    indicator_type = inputs[7]

    global CONTROLS

    CONTROLS = dict(
        outlier=outlier,
        indicator=indicator,
        indicator_type=indicator_type,
        district=district,
        target_year=target_year,
        target_month=target_month,
        reference_year=reference_year,
        reference_month=reference_month,
    )

    global init_data_set

    init_data_set = define_datasets(static=static, dfs=dfs, **CONTROLS)

    ds.switch_data_set(init_data_set)

    return [ds.get_layout()]


@app.callback(
    [
        Output(f"{facility_scatter.my_name}_figure", "figure"),
        Output(f"{facility_scatter.my_name}_fig_title", "children"),
    ],
    [Input(f"{tree_map_district.my_name}_figure", "clickData")],
)
def update_on_click(*inputs):

    # TODO Have that update only teh facility parametr rather than fetchingit all from the controls

    inp = inputs[0]

    try:

        label = inp.get("points")[0].get("label")

        global init_data_set

        init_data_set = define_datasets(
            static=static, dfs=dfs, **CONTROLS, facility=label
        )

        facility_scatter.data = init_data_set
        facility_scatter.figure = facility_scatter._get_figure(facility_scatter.data)
        facility_scatter.figure_title = (
            f"Evolution of $label$ in {label} (click on the graph above to filter)"
        )

    except Exception as e:
        print(e)

    return [facility_scatter.figure, facility_scatter.figure_title]


@app.callback(
    [Output("ds-paginator", "children"), Output("paginator", "children")],
    [Input("dashboard-button", "n_clicks"), Input("reporting-button", "n_clicks")],
)
def change_page(*inputs):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if "dashboard-button" in changed_id:
        ds.data_cards = [
            country_overview_scatter,
            country_overview,
            district_overview_scatter,
            tree_map_district,
            facility_scatter,
        ]
        paginator.dash_clicked = True
    elif "reporting-button" in changed_id:
        ds.data_cards = [
            stacked_bar_reporting_country,
            reporting_map,
            stacked_bar_district,
        ]
        paginator.dash_clicked = False

    return [ds.get_container(), paginator.get_layout()]


@app.callback(
    [
        Output(f"{country_overview_scatter.my_name}_title", "children"),
        Output(f"{district_overview_scatter.my_name}_title", "children"),
        Output(f"{stacked_bar_reporting_country.my_name}_title", "children"),
        Output(f"{tree_map_district.my_name}_title", "children"),
    ],
    [Input(x, y) for (x, y) in callback_ids.items()],
)
def change_titles(*inputs):

    outlier = inputs[0]
    indicator = inputs[1]
    reference_year = inputs[2]
    reference_month = inputs[3]
    target_year = inputs[4]
    target_month = inputs[5]
    district = inputs[6]

    try:
        # Data card 1
        data = country_overview_scatter.data
        data_reference = data.get(reference_year)
        data_target = data.get(target_year)
        perc_first = round(
            (data_target.loc[target_month][0] / data_reference.loc[reference_month][0])
            * 100
        )
    except Exception:
        perc_first = "?"

    country_overview_scatter.title = f"Overview: Across the country, the number of {indicator} changed by {perc_first}% between {reference_month}-{reference_year} and {target_month}-{target_year}"

    try:

        dis_data = district_overview_scatter.data

        dis_data_reference = data.get(reference_year)
        dis_data_target = data.get(target_year)

        dist_perc = round(
            (
                dis_data_target.loc[target_month][0]
                / dis_data_reference.loc[reference_month][0]
            )
            * 100
        )
    except Exception:
        dist_perc = "?"

    district_overview_scatter.title = f"Deep-dive in {district} district: The number of {indicator} changed by {dist_perc}% between {reference_month}-{reference_year} and {target_month}-{target_year}"

    try:
        data_reporting = stacked_bar_reporting_country.data

        date_reporting = datetime(target_year, month_order.index(target_month) + 1, 1)

        try:
            reported_positive = data_reporting.get("Reported a positive number").loc[
                date_reporting
            ][0]
        except Exception:
            reported_positive = 0
        try:
            did_not_report = data_reporting.get(
                "Did not report on their 105:1 form"
            ).loc[date_reporting][0]
        except Exception:
            did_not_report = 0
        try:
            reported_negative = data_reporting.get(
                "Did not report a positive number"
            ).loc[date_reporting][0]
        except Exception:
            reported_negative = 0

        reported_perc = round(
            (
                (reported_positive + reported_negative)
                / (reported_positive + did_not_report + reported_negative)
            )
            * 100
        )
        reported_positive = round(
            (reported_positive / (reported_positive + reported_negative)) * 100
        )
    except Exception:
        reported_perc = "?"
        reported_positive = "?"

    stacked_bar_reporting_country.title = (
        f"Reporting: On {target_month}-{target_year}, around {reported_perc}% of facilities reported on their 105:1 form, and, out of those, {reported_positive}% reported for this {indicator}",
    )

    tree_map_district.title = f"Contribution of individual facilities in {district} district to the total number of {indicator} on {target_month}-{target_year}"

    return [
        country_overview_scatter.title,
        district_overview_scatter.title,
        stacked_bar_reporting_country.title,
        tree_map_district.title,
    ]


@app.callback(
    [Output("fade", "is_in"), Output("fade-button", "children")],
    [Input("fade-button", "n_clicks")],
    [State("fade", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        is_in = True
    out = not is_in
    button_title = "Controls"
    return [out, button_title]


@app.callback(
    [Output("fade2", "is_in"), Output("fade-button2", "children")],
    [Input("fade-button2", "n_clicks")],
    [State("fade2", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clickedppy
        is_in = True
    out2 = not is_in
    button_title2 = "Info"
    return [out2, button_title2]

