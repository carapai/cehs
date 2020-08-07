from coehcs_dashboard_controller import facility_evolution_scatter
import os

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import geopandas as gpd
import pandas as pd
from datetime import datetime
from dash.dependencies import Input, Output, State
from rich import print
from sqlalchemy import create_engine

from coehcs_dashboard_controller import (bar_facilities_country_transform,
                                         bar_facilities_district_transform,
                                         check_index, check_index_dfs,
                                         filter_by_district,
                                         filter_df_by_dates,
                                         filter_df_by_indicator,
                                         filter_df_by_policy,
                                         get_init_data_set,
                                         map_country_overview_transform,
                                         merge_data, remove_columns,
                                         reporting_map_transform,
                                         scatter_country_overview_transform,
                                         scatter_district_overview_transform,
                                         tree_map_district_transform)
from coehcs_dashboard_model import (CardLayout, DatePicker, DatePickerGroup,
                                    SideNav)
from package.components import NestedDropdownGroup
from package.layout.area_card import AreaDataCard
from package.layout.chart_card import ChartDataCard
from package.layout.data_story import DataStory
from package.layout.map_card import MapDataCard

# Data


# Get set of credentials

credentials = {}

for x in os.environ:
    if 'DASH_AUTH' in x:
        login = x.split('DASH_AUTH_')[1]
        password = os.environ.get(x, os.environ.get('SECRET'))
        credentials[login] = password



shapefile = gpd.read_file('./data/shapefiles/shapefile.shp')


DATABASE_URI = os.environ['HEROKU_POSTGRESQL_CYAN_URL']
engine = create_engine(DATABASE_URI)


columns = {x.get('new'): x.get('old') for x in pd.read_sql(
    'SELECT new, old FROM columns_index;', con=engine).to_dict('records')}

data_reporting = pd.read_sql('''SELECT reporting.*, facilities_index.facility_name
                                FROM reporting
                                JOIN facilities_index
                                ON reporting.facility_id = facilities_index.facility_id''', con=engine)

data_outliers = pd.read_sql('''SELECT with_outliers.*, facilities_index.facility_name
                               FROM with_outliers
                               JOIN facilities_index
                               ON with_outliers.facility_id = facilities_index.facility_id''', con=engine)

data_std = pd.read_sql('''SELECT no_outliers_std.*, facilities_index.facility_name
                          FROM no_outliers_std
                          JOIN facilities_index
                          ON no_outliers_std.facility_id = facilities_index.facility_id''',
                       con=engine)

data_iqr = pd.read_sql('''SELECT no_outliers_iqr.*, facilities_index.facility_name
                          FROM no_outliers_iqr
                          JOIN facilities_index
                          ON no_outliers_iqr.facility_id = facilities_index.facility_id''',
                       con=engine)

dfs = {
    'Correct outliers - using standard deviation': data_std,
    'Correct outliers - using interquartile range': data_iqr,
    'Keep outliers': data_outliers,
    'Reporting': data_reporting,
}

indicator_group = pd.read_sql('SELECT * FROM indicator_groups', con=engine)

for key, df in dfs.items():
    df['date'] = pd.to_datetime(df.date, errors='coerce')
    df = df.rename(columns=columns)
    dfs[key] = df


outlier_policy_dropdown_group = NestedDropdownGroup(pd.DataFrame({'Select an outlier correction policy': ['Keep outliers',
                                                                                                          'Correct outliers - using standard deviation',
                                                                                                          'Correct outliers - using interquartile range']}),
                                                    title='Select an outlier correction policy')


outlier_policy_dropdown_group.dropdown_objects[0].value = 'Correct outliers - using standard deviation'


indicator_dropdown_group = NestedDropdownGroup(
    indicator_group, title='Select an indicator')

indicator_dropdown_group.dropdown_objects[0].value = 'EPI'
indicator_dropdown_group.dropdown_objects[1].value = 'DPT3'

month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

years = [2018] * 12 + [2019] * 12 + [2020] * 12

date_columns = pd.DataFrame({'year': years, 'month': month_order*3})

date_columns.columns = ['Target Year', 'Target Month']
target_date = NestedDropdownGroup(
    date_columns.copy(), title='Select target date', vertical=False)

target_date.dropdown_objects[0].value = 2020
target_date.dropdown_objects[1].value = 'May'

date_columns.columns = ['Reference Year', 'Reference Month']
reference_date = NestedDropdownGroup(
    date_columns, title='Select reference date', vertical=False)

reference_date.dropdown_objects[0].value = 2019
reference_date.dropdown_objects[1].value = 'May'

district_control_group = NestedDropdownGroup(data_outliers[['id']].rename(columns={'id': 'Please select a district'}),
                                             title='Select a district')

district_control_group.dropdown_objects[0].value = 'KAMPALA'

side_nav = SideNav([outlier_policy_dropdown_group, indicator_dropdown_group,
                    reference_date, target_date, district_control_group])


global init_data_set
init_data_set = get_init_data_set(dfs.get('Keep outliers'), dfs)

# Data cards


# Scatter plot overview of country 1

country_overview_scatter = ChartDataCard(title='Overview: Across the country, the number of $label$ changed by between 04-2019 and 04-2020',
                                         fig_title='Total number of $label$ across the country',
                                         data=init_data_set,
                                         data_transform=scatter_country_overview_transform,
                                         fig_type='Scatter'
                                         )

country_overview_scatter.set_colors({'fig': {2018: 'rgb(185, 221, 241)',
                                             2019: 'rgb(106, 155, 195)',
                                             2020: 'rgb(200, 19, 60)'}})

# Country map 2


country_overview_map = MapDataCard(
    fig_title='Percentage change in number of $label$ between target and reference date',
    data=init_data_set,
    data_transform=map_country_overview_transform,
    geodata=shapefile,
    locations='id',
    map_tolerance=0.005)


# Scatter district 3


district_overview_scatter = ChartDataCard(title='Deep-dive in the selected district: The number of $label$ changed by % between 05-2019 and 05-2020',
                                          fig_title='Total number of $label$ in the selected district',
                                          data=init_data_set,
                                          data_transform=scatter_district_overview_transform,
                                          fig_type='Scatter')


district_overview_scatter.set_colors({'fig': {2018: 'rgb(185, 221, 241)',
                                              2019: 'rgb(106, 155, 195)',
                                              2020: 'rgb(200, 19, 60)'}})

# Treemap chart 4


tree_map_district = AreaDataCard(title="The contribution of individual facilities in the selected district",
                                 data=init_data_set,
                                 data_transform=tree_map_district_transform,
                                 fig_object='Treemap'
                                 )
tree_map_district.set_colors({'fig': ['#e2d5d1', '#96c0e0', '#3c6792']})

# Scatter for facilities 4.1


facility_scatter = ChartDataCard(fig_title='Evolution of $label$ (click on the graph above to filter)',
                                 data=init_data_set,
                                 data_transform=facility_evolution_scatter)

facility_scatter.set_colors({'fig': {2018: 'rgb(185, 221, 241)',
                                     2019: 'rgb(106, 155, 195)',
                                     2020: 'rgb(200, 19, 60)'}})


# Stacked bar chart 5
stacked_bar_reporting_country = ChartDataCard(title='Reporting: On 05-2020, around % of facilities reported on their 105:1 form, and, out of these % reported for this $label$',
                                              data=init_data_set,
                                              data_transform=bar_facilities_country_transform,
                                              fig_title='Total number of facilities reporting on their 105:1 form and reported a positive number of $label$ in country',
                                              fig_object='Bar'
                                              )

stacked_bar_reporting_country.set_colors(
    {'fig': ['rgb(42, 87, 131)', 'rgb(247, 190, 178)', 'rgb(211, 41, 61)']})

# Reporting map 6


reporting_map = MapDataCard(fig_title='Percentage of reporting facilities that reported on $label$',
                            data=init_data_set,
                            data_transform=reporting_map_transform,
                            geodata=shapefile,
                            locations='id',
                            map_tolerance=0.005
                            )

# Reporting 7


stacked_bar_district = ChartDataCard(data=init_data_set,
                                     data_transform=bar_facilities_district_transform,
                                     fig_title='Total number of facilities reporting on their 105:1 form and reporting on $label$',
                                     fig_object='Bar'  # Relies on the 'overlay' layout barmode parameter for stacking
                                     )

stacked_bar_district.set_colors(
    {'fig': ['rgb(42, 87, 131)', 'rgb(247, 190, 178)', 'rgb(211, 41, 61)']})


ds = DataStory(data_cards=[
    country_overview_scatter,
    country_overview_map,
    district_overview_scatter,
    tree_map_district,
    facility_scatter,
    stacked_bar_reporting_country,
    reporting_map,
    stacked_bar_district
],
    ind_elements=[side_nav],
    footer_image='/static/images/UNICEF-MOH-bottom-resized.jpg',
    title='Continuity of Essential Health Services',
    sub_title='Overview of country and district level health services for MOH Uganda')

app = ds.app

# auth = dash_auth.BasicAuth(
#     app,
#     credentials
# )

callback_ids = {outlier_policy_dropdown_group.dropdown_ids[-1]: 'value',
                indicator_dropdown_group.dropdown_ids[-1]: 'value',
                reference_date.dropdown_ids[0]: 'value',
                reference_date.dropdown_ids[-1]: 'value',
                target_date.dropdown_ids[0]: 'value',
                target_date.dropdown_ids[-1]: 'value',
                district_control_group.dropdown_ids[-1]: 'value'}


@ app.callback(
    [Output('ds-container', 'children')],
    [Input(x, y) for (x, y) in callback_ids.items()]
)
def global_story_callback(*inputs):

    outlier = inputs[0]
    indicator = inputs[1]
    reference_year = inputs[2]
    reference_month = inputs[3]
    target_year = inputs[4]
    target_month = inputs[5]
    district = inputs[6]

    index_columns = ['type', 'id', 'date', 'year',
                     'month', 'facility_id', 'facility_name']

    df = filter_df_by_policy(dfs, outlier)

    df = filter_df_by_indicator(df, indicator, persist_columns=index_columns)

    df_dated = filter_df_by_dates(
        df, target_year, target_month, reference_year, reference_month)

    df_district = filter_by_district(df, district)

    df_facility = df_district[df_district.facility_id ==
                              df_district.facility_id[0]].reset_index(drop=True)

    df_district_dated = filter_by_district(df_dated, district)

    df_reporting = dfs.get('Reporting')

    df_reporting = filter_df_by_indicator(
        df_reporting, indicator, persist_columns=index_columns)

    df_reporting_dated = filter_df_by_dates(
        df_reporting, target_year, target_month, reference_year, reference_month)

    df_reporting_district = filter_by_district(df_reporting, district)

    df_reporting_disctrict_dated = filter_df_by_dates(
        df_reporting_district, target_year, target_month, reference_year, reference_month)

    global init_data_set

    init_data_set = {'country': df,
                     'country_dated': df_dated,
                     'district': df_district,
                     'district_dated': df_district_dated,
                     'reporting_country': df_reporting,
                     'reporting_country_dated': df_reporting_dated,
                     'reporting_district': df_reporting_district,
                     'reporting_district_dated': df_reporting_disctrict_dated,
                     'facility': df_facility}

    ds.switch_data_set(init_data_set)

    return [ds.get_layout()]


@app.callback(
    [
        Output(f'{facility_scatter.my_name}_figure', 'figure'),
        Output(f'{facility_scatter.my_name}_fig_title', 'children')
    ],
    [
        Input(f'{tree_map_district.my_name}_figure', 'clickData')
    ])
def update_on_click_or_hover(*inputs):
    inp = inputs[0]
    global init_data_set
    data_out = init_data_set.get('district').reset_index(drop=True)
    try:
        label = inp.get('points')[0].get('label')
    except Exception:
        label = data_out.facility_name[0]
    data_out = data_out[data_out.facility_name == label].reset_index(drop=True)
    init_data_set['facility'] = data_out
    facility_scatter.data = init_data_set
    facility_scatter.figure = facility_scatter._get_figure(facility_scatter.data)
    facility_scatter.figure_title = f'Evolution of $label$ in {label} (click on the graph above to filter)'
    return [facility_scatter.figure, facility_scatter.figure_title]


@app.callback(
    [
        Output(f'{country_overview_scatter.my_name}_title', 'children'),
        Output(f'{district_overview_scatter.my_name}_title', 'children'),
        Output(f'{stacked_bar_reporting_country.my_name}_title', 'children'),
        Output(f'{tree_map_district.my_name}_title', 'children')
    ],
    [Input(x, y) for (x, y) in callback_ids.items()]
)
def change_titles(*inputs):

    outlier = inputs[0]
    indicator = inputs[1]
    reference_year = inputs[2]
    reference_month = inputs[3]
    target_year = inputs[4]
    target_month = inputs[5]
    district = inputs[6]

    try:
        # Data card 1
        data = country_overview_scatter.data
        data_reference = data.get(reference_year)
        data_target = data.get(target_year)

        perc_first = round(
            data_target.loc[target_month][0] / data_reference.loc[reference_month][0], 0) * 100
    except Exception:
        perc_first = '?'

    country_overview_scatter.title = f'Overview: Across the country, the number of {indicator} changed by {perc_first}% between {reference_month}-{reference_year} and {target_month}-{target_year}'


    try:

        dis_data = district_overview_scatter.data

        dis_data_reference = data.get(reference_year)
        dis_data_target = data.get(target_year)

        dist_perc = round(dis_data_target.loc[target_month][0] /
                          dis_data_reference.loc[reference_month][0], 0) * 100
    except Exception:
        dist_perc = '?'

    district_overview_scatter.title = f'Deep-dive in {district} district: The number of {indicator} changed by {dist_perc}% between {reference_month}-{reference_year} and {target_month}-{target_year}'


    try:
        data_reporting = stacked_bar_reporting_country.data

        date_reporting = datetime(
            target_year, month_order.index(target_month)+1, 1)

        try:
            reported_positive = data_reporting.get(
                'Reported a positive number').loc[date_reporting][0]
        except Exception:
            reported_positive = 0
        try:
            did_not_report = data_reporting.get(
                'Did not report on their 105:1 form').loc[date_reporting][0]
        except Exception:
            did_not_report = 0
        try:
            reported_negative = data_reporting.get(
                'Did not report a positive number').loc[date_reporting][0]
        except Exception:
            reported_negative = 0

        reported_perc = round((reported_positive+reported_negative) /
                              (reported_positive + did_not_report + reported_negative), 0) * 100
        reported_positive = round(
            reported_positive/(reported_positive+reported_negative), 0) * 100
    except Exception:
        reported_perc = '?'
        reported_positive = '?'

    stacked_bar_reporting_country.title = f'Reporting: On {target_month}-{target_year}, around {reported_perc}% of facilities reported on their 105:1 form, and, out of those, {reported_positive}% reported for this {indicator}',

    tree_map_district.title = f"The contribution of individual facilities in {district} district to the total number of {indicator} on {target_month}-{target_year}"

    return [country_overview_scatter.title, district_overview_scatter.title, stacked_bar_reporting_country.title, tree_map_district.title]


@app.callback(
    [Output("fade", "is_in"), Output('fade-button', 'children')],
    [Input("fade-button", "n_clicks")],
    [State("fade", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        is_in = False
    out = not is_in
    button_title = 'Hide controls' if out else 'Show controls'
    return [out, button_title]


# comment out on development
if __name__ == '__main__':
    ds.run(dev=True, host='0.0.0.0')
