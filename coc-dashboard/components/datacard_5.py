from helpers import (filter_df_by_policy,
                     filter_df_by_indicator,
                     reporting_count_transform,
                     index_base_columns,
                     timeit)


# @timeit
def bar_reporting_country_data(dfs, static, indicator, **kwargs):

    df_reporting = filter_df_by_policy(dfs, 'Reporting')

    df_reporting = filter_df_by_indicator(
        df_reporting, indicator, persist_columns=index_base_columns)

    return df_reporting


@timeit
def bar_reporting_country_plot(data):

    data_in = data.get('reporting_country')
    data_out = reporting_count_transform(data_in.copy())

    return data_out
