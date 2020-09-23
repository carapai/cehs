
import pandas as pd

from helpers import (filter_df_by_policy,
                     filter_df_by_indicator,
                     filter_by_district,
                     get_district_sum,
                     get_percentage,
                     get_sub_dfs,
                     check_index,
                     month_order,
                     index_base_columns,
                     timeit)


# @timeit
def scatter_district_data(dfs, static, outlier, indicator, indicator_type,
                          district, **kwargs):
    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(
        df, indicator, persist_columns=index_base_columns)

    df_district = filter_by_district(df, district)
    df_district = get_district_sum(df_district, indicator)
    df_district = get_percentage(df_district,
                                 static.get('population data'),
                                 static.get('target population type'),
                                 indicator_type,
                                 indicator)

    return df_district


@timeit
def scatter_district_plot(df):

    df_district = df.get('district')

    df_district = df_district[df_district[df_district.columns[0]] > 0]

    df_district = get_sub_dfs(
        df_district, 'year', [2018, 2019, 2020], 'month', month_order)

    return df_district
