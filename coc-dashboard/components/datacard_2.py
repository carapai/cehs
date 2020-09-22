import pandas as pd

from helpers import (filter_df_by_policy,
                     filter_df_by_indicator,
                     filter_df_by_dates,
                     get_percentage,
                     check_index,
                     index_base_columns,
                     timeit,
                     month_order)


@timeit
def map_bar_country_dated_data(dfs, static, outlier, indicator, indicator_type,
                               target_year, target_month, reference_year, reference_month):

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(
        df, indicator, persist_columns=index_base_columns)

    data_in = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month)

    data_in = get_percentage(data_in,
                             static.get('population data'),
                             static.get('target population type'),
                             indicator_type,
                             indicator)

    data_in.reset_index(inplace=True)

    # TODO updat teh filter by data function so that this step is no longer needed

    mask = (((data_in.year == int(reference_year)) & (data_in.month == reference_month))
            | ((data_in.year == int(target_year)) & (data_in.month == target_month)))

    data_in = data_in[mask]

    data_in = data_in.groupby(
        by=['id', 'year', 'month'], as_index=False).agg({indicator: 'sum'})
    data_in = data_in.pivot_table(columns='year', values=indicator, index='id')

    data_in[indicator] = (data_in[int(target_year)] -
                          data_in[int(reference_year)]) / data_in[int(reference_year)] * 100
    data_in[indicator] = data_in[indicator].apply(lambda x: round(x, 2))

    data_in = data_in[[indicator]].reset_index()
    data_in['id'] = data_in['id'].astype(str)
    data_in = data_in.set_index('id')
    data_out = data_in[~pd.isna(data_in[indicator])]

    return data_out


@ timeit
def map_country_dated_plot(data):

    data = data.get('dated')

    data_out = {f'Change between reference and target date': data}

    return data_out


@ timeit
def bar_country_dated_plot(data):

    data = data.get('dated')

    data[data.columns[0]] = data[data.columns[0]]/100

    data['rank'] = data.rank(ascending=True)
    data = data[data['rank'] < 11].sort_values(by='rank')
    data.drop('rank', axis=1, inplace=True)
    data_out = {'Top/Bottom 10': data}

    return data_out
