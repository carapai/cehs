
import pandas as pd
from rich import print
import numpy as np
from datetime import datetime
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Filtering methods


def filter_df_by_policy(dfs, key):
    df = dfs.get(key)
    return df


def filter_df_by_indicator(df, indicator, persist_columns=[]):
    columns_to_keep = persist_columns + [indicator]
    df = df[columns_to_keep]

    return df


def filter_df_by_dates(df, target_year, target_month, reference_year, reference_month):
    min_date = None
    max_date = None
    reverse = False

    df = df.sort_values(['date'])

    if target_year and target_month:
        target_date = datetime(int(target_year), int(
            month_order.index(target_month) + 1), 1)
    if reference_year and reference_month:
        reference_date = datetime(int(reference_year), int(
            month_order.index(reference_month) + 1), 1)
    if reference_date <= target_date:
        max_date = target_date
        min_date = reference_date
    elif target_date < reference_date:
        max_date = reference_date
        min_date = target_date
        reverse = True
    if min_date:
        min_mask = (df.date >= min_date)
        df = df.loc[min_mask].reset_index(drop=True)
    if max_date:
        max_mask = (df.date <= max_date)
        df = df.loc[max_mask].reset_index(drop=True)
    if reverse:
        df = df.reindex(index=df.index[::-1])
    return df


def filter_by_district(df, district):
    mask = (df.id == district)
    df = df.loc[mask].reset_index(drop=True)
    return df

# Data transformations


def check_index(df, index=['type', 'id', 'date', 'year', 'month', 'facility_id', 'facility_name']):
    '''
    Check that the dataframe is formatted in the expected way, with expected indeces. Restructure the dataframe (set the indeces) if this is not the case.
    '''
    if df.index.values != index:
        print('Checking index')
        # Set the indeces
        df = df.reset_index(drop=True).set_index(index)
    return df


def check_index_dfs(dfs, index=['id', 'date', 'year', 'month', 'facility_id', 'facility_name']):
    '''
    Check that the dataframe is formatted in the expected way, with expected indeces. Restructure the dataframe (set the indeces) if this is not the case.
    '''
    for key, df in dfs.items():
        # Check the indeces
        if df.index.values != index:
            # Set the indeces
            dfs[key] = df.set_index(index)
    return dfs


def merge_data(dfs, static_data, shared_column='facility_id'):
    # If there's shared column ('facility_id'), add/merge data from static_data
    for key, df in dfs.items():
        if shared_column in df.columns:
            df = pd.merge(df, static_data)
        dfs[key] = df
    return dfs


def remove_columns(dfs, columns):
    '''
    Remove unnecessary columns from the dictionary's dataframes
    '''
    clean_dfs = {}
    for key, df in dfs.items():
        # TODO: Check if the columns are present before asking to drop them (or is this done automatically in .drop() ??)
        df = df.drop(columns=columns)
        clean_dfs[key] = df
    return clean_dfs


def get_one_dict_level(dicts, with_key_prefix=True):
    '''
    Get the sub-dictionaries as first-dictionary entries
    '''
    dfs = {}
    for dict_key, dict_dict in dicts.items():
        for df_key, df in dict_dict.items():
            key = f'{dict_key}_{df_key}' if with_key_prefix else f'{df_key}'
            dfs[key] = df
    return dfs


def get_sub_dfs(df, select_index, values, new_index, order=None):
    '''
    Extract and return a dictionary of dictionaries splitting each original dictionary df entry into traces based on values
    '''

    traces = {}
    for value in values:
        sub_df = df[df.index.get_level_values(select_index) == value]
        sub_df = sub_df.groupby(new_index).sum()
        if order:
            sub_df = sub_df.reindex(order)
        traces[value] = sub_df

    return traces


def get_init_data_set(df, dfs={}):
    country = df
    district = df[df.id == 'KAMPALA']
    facility = district[district.facility_name == 'Royal Health Care HC II']
    country_dated = df[(df.date >= datetime(2019, 4, 1)) &
                       (df.date <= datetime(2020, 4, 1))]
    district_dated = district[(district.date >= datetime(
        2019, 4, 1)) & (district.date <= datetime(2020, 4, 1))]
    rep_df = dfs.get('Reporting')
    rep_df_dated = rep_df[(rep_df.date >= datetime(2019, 4, 1)) & (
        rep_df.date <= datetime(2020, 4, 1))]
    rep_df_district = rep_df[rep_df.id == 'KAMPALA']
    rep_df_district_dated = rep_df_district[(rep_df_district.date >= datetime(
        2019, 4, 1)) & (rep_df_district.date <= datetime(2020, 4, 1))]

    init_data_set = {'country': country,
                     'district': district,
                     'country_dated': country_dated,
                     'district_dated': district_dated,
                     'reporting_country': rep_df,
                     'reporting_country_dated': rep_df_dated,
                     'reporting_district': rep_df_district,
                     'reporting_district_dated': rep_df_district_dated,
                     'facility':facility}
    return init_data_set

###


def get_index_subset_dfs(df, value, select_index='id'):  # or select_index=0
    '''
    Filter the data by index value, return dictionary of dataframes with only this index value
    '''
    df[df[select_index] == value]
    return df


def group_by_date_agg(df, y_1=2018, y_2=2019, month='Mar', agg_val='id'):
    '''
    Group the dataframe by years and aggregate
    '''
    # Check that there is a year and month column
    # TODO: Add assert
    # get_index_subset_dfs(dfs, select_index='month', value=month)
    df = df[df['month'] == month]
    df = get_sub_dfs(df, 'year', [y_1, y_2], agg_val)
    return df


def get_change_df(dfs, columns=None):
    '''
    Get a df of change between values of a column of two dataframes (in a dictionary)
    '''
    # TODO: Refactor to work with dictionaries within a dictionary
    dfs_vals = list(dfs.values())
    keys = list(dfs.keys())
    if not columns:
        columns = dfs_vals[0].columns
    df = pd.DataFrame()
    assert len(
        dfs) == 2, 'To calculate the change, there must be TWO (not more or less) dataframes'
    for col in columns:
        df[col] = round(
            ((dfs_vals[1][col] - dfs_vals[0][col]) / dfs_vals[0][col])*100, 2)
    change_dict = {f'{str(keys[0])}_{str(keys[1])}_change': df}
    return change_dict


def reporting_count_transform(data):
    """
    Counts occurance of type of reporting label for each date, returning dictionary
    """
    # Set index
    data = check_index(data)
    # Remove unneccesary index values
    data = data.droplevel(['type', 'id'])
    # Count number of positive_indic
    df_positive = get_num(data, 'positive_indic')
    # Count number of no_positive_indic
    df_no_positive = get_num(data, 'no_positive_indic')
    # Count number of no_form_report
    df_no_form_report = get_num(data, 'no_form_report')

    data = {
        'Reported a positive number': df_positive,
        'Did not report a positive number': df_no_positive,
        'Did not report on their 105:1 form': df_no_form_report,
    }
    return data


def get_num(df, value='positive_indic'):
    """
    Gets a dataframe of the count of the specified value for each column; expects index formatting including date and id
    """
    df_count_all = []
    for date in list((df.index.get_level_values('date')).unique()):
        count_for_date = (df.loc[date] == value).sum()
        df_count_for_date = (pd.DataFrame(count_for_date)).transpose()
        df_count_for_date.index = [date]
        df_count_all.append(df_count_for_date)
    new_df = pd.concat(df_count_all)
    return new_df

# data card functions

# Data Card 1


def scatter_country_overview_transform(data):
    print('Getting data for the data card 1')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data_out = check_index(data.get('country'))
    data_out = data_out[data_out[data_out.columns[0]] > 0]
    data_out = get_sub_dfs(
        data_out, 'year', [2018, 2019, 2020], 'month', month_order)
    return data_out


# Data Card 2
def map_country_overview_transform(data):
    print('Getting data for the data card 2')

    data_in = data.get('country_dated')
    # Get the first date and the last one of the df
    # df ordered according to reference (at top) and target date (at end)
    first_date = data_in.date.iloc[0].to_pydatetime()
    last_date = data_in.date.iloc[-1].to_pydatetime()

    # Seperate dataframe by dates
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    mask = ((data_in.year == first_date.year) & (data_in.month == month_order[first_date.month - 1])) \
        | ((data_in.year == last_date.year) & (data_in.month == month_order[last_date.month-1]))

    data_in = data_in[mask]
    data_in = check_index(data_in)
    val_col = data_in.columns[0]
    data_in = data_in[[val_col]]
    data_in = data_in.reset_index()
    data_in = data_in.groupby(by=['id', 'year', 'month']).sum().reset_index()
    data_in = data_in.pivot_table(columns='year', values=val_col, index='id')


    data_in[val_col] = (data_in[last_date.year] -
                        data_in[first_date.year]) / data_in[first_date.year] * 100
    data_in[val_col] = data_in[val_col].apply(lambda x: round(x, 2))

    data_in = data_in[[val_col]].reset_index()
    data_in['id'] = data_in['id'].astype(str)
    data_in = data_in.set_index('id')
    data_in = data_in[~pd.isna(data_in[val_col])]
    data_out = {
        f'Change between {first_date.year} {first_date.month} and {last_date.year} {last_date.month}': data_in}

    return data_out

# Data card 3


def scatter_district_overview_transform(data):
    print('Getting data for the data card 3')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data_out = check_index(data.get('district'))
    data_out = data_out[data_out[data_out.columns[0]] > 0]
    data_out = get_sub_dfs(
        data_out, 'year', [2018, 2019, 2020], 'month', month_order)
    return data_out


# Data card 4
def tree_map_district_transform(data):
    print('Getting data for the data card 4')
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

# Data card 4.1
def facility_evolution_scatter(data):
    data = data.get('facility')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = check_index(data)
    data = data[data[data.columns[0]] > 0]
    data = get_sub_dfs(
        data, 'year', [2018, 2019, 2020], 'month', month_order)

    return data
# Data card 5


def bar_facilities_country_transform(data):
    print('Getting data for the data card 5')
    data_in = data.get('reporting_country')
    data_out = reporting_count_transform(data_in.copy())
    return data_out


# Data card 6
def reporting_map_transform(data):
    print('Getting data for data card 6')
    data_in = data.get('reporting_country_dated')

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
        report_rate = round(reported_facilities / total_facilities, 2)
        districts.append(district)
        reporting.append(report_rate*100)

    reporting_df = pd.DataFrame({'id': districts, 'Reporting rate': reporting})
    reporting_df = reporting_df.set_index('id')

    data_out = {
        f"Reporting rate during {last_date.to_pydatetime().strftime('%B %Y')}": reporting_df}
    return data_out

# Data card 7


def bar_facilities_district_transform(data):
    print('Getting data for data card 7')
    data_in = data.get('reporting_district')
    data_out = reporting_count_transform(data_in.copy())
    return data_out
