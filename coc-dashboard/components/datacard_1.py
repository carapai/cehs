
import pandas as pd

from helpers import (filter_df_by_policy,
                     filter_df_by_indicator,
                     get_national_sum,
                     get_percentage,
                     get_sub_dfs,
                     month_order,
                     index_base_columns,
                     timeit)


@timeit
def scatter_country_data(dfs, static, outlier, indicator, indicator_type, **kwargs):

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(
        df, indicator, persist_columns=index_base_columns)

    df_country = get_national_sum(df, indicator)

    df_country = get_percentage(df_country,
                                static.get('population data'),
                                static.get('target population type'),
                                indicator_type,
                                indicator, all_country=True)

    return df_country


@timeit
def scatter_country_plot(df):

    df_country = df.get('country')

    df_country = df_country[df_country[df_country.columns[0]] > 0]

    df_country = get_sub_dfs(
        df_country, 'year', [2018, 2019, 2020], 'month', month_order)

    return df_country
