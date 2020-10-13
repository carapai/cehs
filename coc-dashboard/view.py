import os
from datetime import datetime
from pprint import pprint as print

import dash
import dash_auth
import dash_core_components as dcc
import geopandas as gpd
import pandas as pd

import store

from store import (
    credentials,
    data_outliers,
    define_datasets,
    download_file,
    indicator_groups,
    month_order,
    side_nav,
    static,
)

from components import (
    country_overview,
    country_overview_scatter,
    district_overview_scatter,
    facility_scatter,
    reporting_map,
    stacked_bar_district,
    stacked_bar_reporting_country,
    tree_map_district,
)

from model import CardLayout, Datadownload
from package.components.methodology_section import MethodologySection
from package.components.nested_dropdown_group import NestedDropdownGroup
from package.layout.data_story import DataStory

##############
#   LAYOUT   #
##############

ds = DataStory(
    data_cards=[
        country_overview_scatter,
        country_overview,
        district_overview_scatter,
        tree_map_district,
        facility_scatter,
    ],
    ind_elements=[side_nav],
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
