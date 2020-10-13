import pandas as pd
from model import Navbar

from store.helpers import month_order
from store.static_info import meth_data
from .database import Database
from package.components.nested_dropdown_group import NestedDropdownGroup
from package.components.methodology_section import MethodologySection

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DEFAULTS = {
    "default_outlier": os.environ["OUTLIER"],
    "default_indicator": os.environ["INDICATOR"],
    "default_indicator_group": os.environ["INDICATOR_GROUP"],
    "default_district": os.environ["DISTRICT"],
    "default_target_year": os.environ["TARGET_YEAR"],
    "default_target_month": os.environ["TARGET_MONTH"],
    "default_reference_year": os.environ["REFERENCE_YEAR"],
    "default_reference_month": os.environ["REFERENCE_MONTH"],
}


def initiate_dropdowns():

    db = Database()

    # Initiate data selection dropdowns

    max_date = db.raw_data.get("value_raw").date.max()
    (max_year, max_month_number) = (max_date.year, max_date.month)
    max_month = month_order[max_month_number - 1]

    years = [2018] * 12 + [2019] * 12 + [2020] * max_month_number

    date_columns = pd.DataFrame(
        {"year": years, "month": month_order * 2 + month_order[:max_month_number]}
    )

    date_columns.year = date_columns.year.astype(str)

    date_columns.columns = ["Target Year", "Target Month"]
    target_date = NestedDropdownGroup(
        date_columns.copy(), title="Select target date", vertical=False
    )

    date_columns.columns = ["Reference Year", "Reference Month"]
    reference_date = NestedDropdownGroup(
        date_columns, title="Select reference date", vertical=False
    )

    # Initiate outlier policy dropdown

    outlier_policy_dropdown_group = NestedDropdownGroup(
        pd.DataFrame(
            {
                "Select an outlier correction policy": [
                    "Keep outliers",
                    "Correct outliers - using standard deviation",
                    "Correct outliers - using interquartile range",
                ]
            }
        ),
        title="Select an outlier correction policy",
    )

    indicator_dropdown_group = NestedDropdownGroup(
        db.indicator_dropdowns, title="Select an indicator"
    )

    district_control_group = NestedDropdownGroup(
        pd.DataFrame({"Select a district": db.districts}),
        title="Select a district",
    )

    methodology_layout = MethodologySection(
        title="Methodology", data=meth_data(db.fetch_date)
    )

    side_nav = Navbar(
        elements=[
            outlier_policy_dropdown_group,
            indicator_dropdown_group,
            reference_date,
            target_date,
            district_control_group,
        ],
        methodology=[methodology_layout],
    )

    return (
        side_nav,
        outlier_policy_dropdown_group,
        indicator_dropdown_group,
        reference_date,
        target_date,
        district_control_group,
    )


def set_dropdown_defaults(
    outlier_policy_dropdown_group,
    target_date,
    reference_date,
    indicator_dropdown_group,
    district_control_group,
):
    outlier_policy_dropdown_group.dropdown_objects[0].value = DEFAULTS.get(
        "default_outlier"
    )

    target_date.dropdown_objects[0].value = DEFAULTS.get("default_target_year")
    target_date.dropdown_objects[1].value = DEFAULTS.get("default_target_month")

    indicator_dropdown_group.dropdown_objects[0].value = DEFAULTS.get(
        "default_indicator_group"
    )
    indicator_dropdown_group.dropdown_objects[1].value = DEFAULTS.get(
        "default_indicator"
    )

    reference_date.dropdown_objects[0].value = DEFAULTS.get("default_reference_year")
    reference_date.dropdown_objects[1].value = DEFAULTS.get("default_reference_month")

    district_control_group.dropdown_objects[0].value = DEFAULTS.get("default_district")
