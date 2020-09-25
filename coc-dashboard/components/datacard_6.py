import pandas as pd

from helpers import (filter_df_by_policy,
                     filter_df_by_indicator,
                     reporting_count_transform,
                     filter_df_by_dates,
                     index_base_columns,
                     check_index,
                     timeit)


# @timeit
def map_reporting_dated_data(dfs, static, *, indicator, target_year, target_month, reference_year, reference_month, **kwargs):

    df_reporting = filter_df_by_policy(dfs, 'Reporting')

    df_reporting = filter_df_by_indicator(
        df_reporting, indicator, persist_columns=index_base_columns)

    df_reporting_dated = filter_df_by_dates(
        df_reporting, target_year, target_month, reference_year, reference_month)

    return df_reporting_dated


@timeit
def map_reporting_dated_plot(data):

    data_in = data.get('reporting_dated')

    last_date = data_in.date.max()

    last_date_df = data_in[data_in.date == last_date]

    last_date_df = check_index(last_date_df)

    val_col = last_date_df.columns[0]

    last_date_df = last_date_df.reset_index()

    districts = []
    reporting = []
    for district in last_date_df.id.unique():
        districtal_df = last_date_df[last_date_df.id == district]
        total_facilities = (districtal_df[val_col] != 'not_expected').sum()
        reported_facilities = len(
            districtal_df[districtal_df[val_col] == 'positive_indic'])
        report_rate = round((reported_facilities / total_facilities)*100, 2)
        districts.append(district)
        reporting.append(report_rate)

    reporting_df = pd.DataFrame({'id': districts, 'Reporting rate': reporting})
    reporting_df = reporting_df.set_index('id')

    data_out = {
        f"Reporting rate during {last_date.to_pydatetime().strftime('%B %Y')}": reporting_df}

    return data_out
