import pandas as pd
import inspect as ip

from store.helpers import timeit
from store.database import Database

from .cards_mutations import (
    scatter_country_data,
    map_bar_country_dated_data,
    scatter_district_data,
    tree_map_district_dated_data,
    scatter_facility_data,
    bar_reporting_country_data,
    map_reporting_dated_data,
    scatter_reporting_district_data,
    # indicator_group,
)

# Define which function corresponds to which object

# TODO find a smart way to iterate through imports rather than repeatthe list manually

FUNC_DICT = {
    "country": scatter_country_data,
    "dated": map_bar_country_dated_data,
    "district": scatter_district_data,
    "district_dated": tree_map_district_dated_data,
    "facility": scatter_facility_data,
    "reporting_country": bar_reporting_country_data,
    "reporting_dated": map_reporting_dated_data,
    "reporting_district": scatter_reporting_district_data,
    # "indicator_group": indicator_group,
}

FUNC_DF = pd.DataFrame.from_dict(FUNC_DICT, orient="index").rename(
    columns={0: "function"}
)

FUNC_DF["args"] = None

for i in FUNC_DF.index:
    f = FUNC_DF.loc[i, "function"]
    args = ip.getfullargspec(f)[4]
    FUNC_DF.loc[i, "args"] = args


@timeit
def define_datasets(controls, last_controls=None):

    db = Database()

    if not last_controls:

        for dataset_name in FUNC_DF.index:
            db.include_dataset(
                dataset_name, FUNC_DF.loc[dataset_name, "function"](**controls)
            )

    else:

        new = pd.DataFrame.from_dict(controls, orient="index")
        last = pd.DataFrame.from_dict(last_controls, orient="index")
        changed = new[(new != last).any(1)]
        changed_keys = set(changed.index)

        for dataset_name in FUNC_DF.index:
            args = set(FUNC_DF.loc[dataset_name, "args"])
            if len(args.intersection(changed_keys)) > 0:
                db.include_dataset(
                    dataset_name, FUNC_DF.loc[dataset_name, "function"](**controls)
                )
                func_name = str(FUNC_DF.loc[dataset_name, "function"]).split(" ")[1]
                print(f"ran function {func_name}")

    return db.datasets
