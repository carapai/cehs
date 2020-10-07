import os
from datetime import datetime

from pprint import pprint as print

import dash
import dash_auth
import dash_core_components as dcc
import geopandas as gpd
import pandas as pd

from store import define_datasets
from dropdown import initiate_dropdowns
from store import month_order
from model import CardLayout, Datadownload, Methodology, Paginator
from package.layout.data_story import DataStory
from package.components.methodology_section import MethodologySection
from package.components.nested_dropdown_group import NestedDropdownGroup

from store import download_file, meth_data

from store import (
    credentials,
    meth_date,
    indicator_group,
    data_outliers,
    static,
    side_nav,
)

from components import (
    country_overview_scatter,
    country_overview,
    district_overview_scatter,
    facility_scatter,
    stacked_bar_reporting_country,
    reporting_map,
    stacked_bar_district,
    tree_map_district,
)


download_button = Datadownload()


methodology_layout = MethodologySection(
    title="Methodology", data=meth_data(meth_date))
methodology = Methodology([methodology_layout])


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
