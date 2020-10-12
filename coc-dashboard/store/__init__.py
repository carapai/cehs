import os

from .helpers import *
from .dropdown import initiate_dropdowns, set_dropdown_defaults
from .database import Database


# READ FROM DATABASE

DATABASE_URI = os.environ["HEROKU_POSTGRESQL_CYAN_URL"]

db = Database(DATABASE_URI)


dropdown_filters = {
    "Correct outliers - using standard deviation": "data_std",
    "Correct outliers - using interquartile range": "data_iqr",
    "Keep outliers": "data_raw",
    "Reporting": "data_rep",
}

db.filter_by_policy = lambda outlier: getattr(Database(), dropdown_filters.get(outlier))

db.filter_by_indicator = lambda df, indicator: df[
    df.indicator_name == indicator
].reset_index(drop=True)


# STATIC DATA
from .static_info import *
from .geopopulation import shapefile, static

# NAVIGATION

(
    side_nav,
    outlier_policy_dropdown_group,
    indicator_dropdown_group,
    reference_date,
    target_date,
    district_control_group,
) = initiate_dropdowns()

set_dropdown_defaults(
    outlier_policy_dropdown_group,
    target_date,
    reference_date,
    indicator_dropdown_group,
    district_control_group,
)

CONTROLS = dict(
    outlier=outlier_policy_dropdown_group.dropdown_objects[0].value,
    indicator=indicator_dropdown_group.dropdown_objects[-1].value,
    # indicator_type=indicator_dropdown_group.dropdown_objects[0].value,
    district=district_control_group.dropdown_objects[0].value,
    target_year=target_date.dropdown_objects[0].value,
    target_month=target_date.dropdown_objects[1].value,
    reference_year=reference_date.dropdown_objects[0].value,
    reference_month=reference_date.dropdown_objects[1].value,
    facility=None,
    indicator_group=indicator_dropdown_group.dropdown_objects[0].value,
)

print("Init control dict")
print(CONTROLS)

LAST_CONTROLS = {}

# CREDENTIALS

credentials = {}

for x in os.environ:
    if "DASH_AUTH" in x:
        login = x.split("DASH_AUTH_")[1]
        password = os.environ.get(x, os.environ.get("SECRET"))
        credentials[login] = password

# GLOBAL DATASET

from .define_datasets import define_datasets

init_data_set = define_datasets(controls=CONTROLS)
