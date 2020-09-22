
import pandas as pd

from helpers import timeit

from components.datacard_1 import scatter_country_data
from components.datacard_2 import map_bar_country_dated_data
from components.datacard_3 import scatter_district_data
from components.datacard_4 import tree_map_district_dated_data
from components.datacard_4 import scatter_facility_data
from components.datacard_5 import bar_reporting_country_data
from components.datacard_6 import map_reporting_dated_data
from components.datacard_7 import scatter_reporting_district_data


@timeit
def define_datasets(static, dfs, outlier,
                    indicator, indicator_type,
                    target_year, target_month, reference_year, reference_month,
                    district, facility=None):

    # TODO Find a better way to reference the args in the functionsto to avoid repetitions
    # Use a dict, psoobily add a parameters for whcih to updte
    # Add the dataset as inputto updte
    # TODO Make it more ressorce efficient by only updating what needs updating
    # Make all of those if > only change if value has changed
    # Need to keep the state of the value in an object
    # This object can be (1)

    country = scatter_country_data(dfs, static, outlier,
                                   indicator, indicator_type)

    dated = map_bar_country_dated_data(dfs, static, outlier, indicator, indicator_type,
                                       target_year, target_month, reference_year, reference_month)

    districts = scatter_district_data(dfs, static, outlier,
                                      indicator, indicator_type,
                                      district)

    district_dated = tree_map_district_dated_data(static, dfs, outlier,
                                                  indicator, district,
                                                  target_year, target_month,
                                                  reference_year, reference_month)

    facility = scatter_facility_data(static, dfs, outlier,
                                     indicator, district, facility)

    reporting = bar_reporting_country_data(dfs, indicator)

    reporting_dated = map_reporting_dated_data(
        dfs, indicator, target_year, target_month, reference_year, reference_month)

    reporting_district = scatter_reporting_district_data(
        dfs, indicator, district)

    datasets = {'country': country,
                'dated': dated,
                'district': districts,
                'district_dated': district_dated,
                'facility': facility,
                'reporting_country': reporting,
                'reporting_dated': reporting_dated,
                'reporting_district': reporting_district}

    return datasets
