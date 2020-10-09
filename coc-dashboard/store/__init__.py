from sqlalchemy import create_engine

from .helpers import *
from .define_datasets import define_datasets
from .geopopulation import static, shapefile
from .read_data import read_data
from .static_info import *
import os
from dropdown import initiate_dropdowns, set_dropdown_defaults


# READ FROM DATABASE

DATABASE_URI = os.environ["HEROKU_POSTGRESQL_CYAN_URL"]
engine = create_engine(DATABASE_URI)

columns, data_reporting, data_outliers, data_std, data_iqr, indicator_group = read_data(
    engine, test=True
)

dfs = {
    "Correct outliers - using standard deviation": data_std,
    "Correct outliers - using interquartile range": data_iqr,
    "Keep outliers": data_outliers,
    "Reporting": data_reporting,
}

for key, df in dfs.items():
    df["date"] = pd.to_datetime(df.date, errors="coerce")
    dfs[key] = df

# NAVIGATION

(
    side_nav,
    outlier_policy_dropdown_group,
    indicator_dropdown_group,
    reference_date,
    target_date,
    district_control_group,
) = initiate_dropdowns(data_outliers, indicator_group)

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

init_data_set = define_datasets(static=static, dfs=dfs, controls=CONTROLS)
