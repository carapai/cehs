import pandas as pd
import inspect as ip

from store.helpers import timeit

from .cards_mutations import (
    scatter_country_data,
    map_bar_country_dated_data,
    scatter_district_data,
    tree_map_district_dated_data,
    scatter_facility_data,
    bar_reporting_country_data,
    map_reporting_dated_data,
    scatter_reporting_district_data,
    indicator_group,
)

# Define which function corresponds to which object

# TODO find a smart way to iterate through imports rather than repeatthe list manually

#args = ip.getfullargspec(scatter_country_data)[0]

FUNC_DICT = {
    "country": scatter_country_data,
    "dated": map_bar_country_dated_data,
    "district": scatter_district_data,
    "district_dated": tree_map_district_dated_data,
    "facility": scatter_facility_data,
    "reporting_country": bar_reporting_country_data,
    "reporting_dated": map_reporting_dated_data,
    "reporting_district": scatter_reporting_district_data,
    "indicator_group": indicator_group}

FUNC_DF = pd.DataFrame.from_dict(
    FUNC_DICT, orient='index').rename(columns={0: "function"})

FUNC_DF['args'] = None

for i in FUNC_DF.index:
    f = FUNC_DF.loc[i, 'function']
    args = ip.getfullargspec(f)[4]
    FUNC_DF.loc[i, 'args'] = args


@timeit
def define_datasets(static, dfs, controls, last_controls={}, datasets={}):

    if last_controls == {}:

        for i in FUNC_DF.index:
            datasets[i] = FUNC_DF.loc[i, "function"](dfs, static, **controls)

    else:

        new = pd.DataFrame.from_dict(controls, orient="index")
        last = pd.DataFrame.from_dict(last_controls, orient="index")
        changed = new[(new != last).any(1)]
        changed_keys = set(changed.index)

        for i in FUNC_DF.index:
            args = set(FUNC_DF.loc[i, 'args'])
            if len(args.intersection(changed_keys)) > 0:
                datasets[i] = FUNC_DF.loc[i, "function"](
                    dfs, static, **controls)
                func_name = str(FUNC_DF.loc[i, "function"]).split(" ")[1]
                print(f"ran function {func_name}")

    return datasets
