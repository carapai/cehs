
import pandas as pd
import numpy as np

from helpers import (filter_df_by_policy,
                     filter_df_by_indicator,
                     filter_by_district,
                     filter_df_by_dates,
                     get_sub_dfs,
                     check_index,
                     month_order,
                     index_base_columns,
                     timeit)


# @timeit
def tree_map_district_dated_data(static, dfs, outlier,
                                 indicator, district,
                                 target_year, target_month,
                                 reference_year, reference_month):

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(
        df, indicator, persist_columns=index_base_columns)

    # TODO check how the date function works such that it shows only target date

    df_district_dated = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month)

    df_district_dated = filter_by_district(df_district_dated, district)

    return df_district_dated


@timeit
def scatter_facility_data(static, dfs, outlier,
                          indicator, district, facility):

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(
        df, indicator, persist_columns=index_base_columns)

    df_facility = filter_by_district(df, district)

    # TODO Reorder such that its the one facility with the on selected data max value that shows

    if facility:
        df_facility = df_facility[df_facility.facility_name == facility].reset_index(
            drop=True)
    else:
        df_facility = df_facility[df_facility.facility_name ==
                                  df_facility.facility_name[0]].reset_index(drop=True)

    return df_facility


@timeit
def tree_map_district_dated_plot(data):

    data_in = data.get('district_dated')
    data_in = check_index(data_in)
    val_col = data_in.columns[0]
    data_in[val_col] = data_in[val_col].apply(
        lambda x: int(x) if pd.notna(x) else 0)
    data_in = data_in.reset_index()
    data_in = data_in[data_in.date == data_in.date.max()].reset_index()
    district_name = data_in.id[0]
    data_tree = data_in.pivot_table(
        values=val_col,
        index=['facility_name'],
        columns='date',
        aggfunc=np.sum)
    data_out = {district_name: data_tree}
    return data_out


@timeit
def scatter_facility_plot(data):
    data = data.get('facility')

    data = check_index(data)
    data = data[data[data.columns[0]] > 0]
    data = get_sub_dfs(
        data, 'year', [2018, 2019, 2020], 'month', month_order)

    return data
