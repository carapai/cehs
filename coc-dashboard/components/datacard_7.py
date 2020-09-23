from helpers import (filter_df_by_policy,
                     filter_df_by_indicator,
                     filter_by_district,
                     reporting_count_transform,
                     index_base_columns,
                     timeit)


# @timeit
def scatter_reporting_district_data(dfs, indicator, district):

    df_reporting = filter_df_by_policy(dfs, 'Reporting')

    df_reporting = filter_df_by_indicator(
        df_reporting, indicator, persist_columns=index_base_columns)

    df_reporting_district = filter_by_district(df_reporting, district)

    return df_reporting_district


@timeit
def scatter_reporting_district_plot(data):

    data_in = data.get('reporting_district')
    data_out = reporting_count_transform(data_in.copy())

    return data_out
