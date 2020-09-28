import os
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
import geopandas as gpd


load_dotenv(find_dotenv())

credentials = {}

for x in os.environ:
    if 'DASH_AUTH' in x:
        login = x.split('DASH_AUTH_')[1]
        password = os.environ.get(x, os.environ.get('SECRET'))
        credentials[login] = password

# TODO Have those paths defined ina  better place than in teh code

columns_mapping_file = './coc-dashboard/data/columns.csv'
data_outliers_file = './coc-dashboard/data/outliers.csv'
data_reporting_file = './coc-dashboard/data/reporting.csv'
data_std_file = './coc-dashboard/data/std.csv'
data_iqr_file = './coc-dashboard/data/iqr.csv'
indicator_group_file = './coc-dashboard/data/groups.csv'


def read_data(engine, test=False):
    # TODO delete references to test
    if test == False:
        try:
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
            indicator_group = pd.read_sql(
                'SELECT * FROM indicator_groups', con=engine)
        except Exception as e:
            columns = {x.get('new'): x.get('old') for x in pd.read_csv(
                columns_mapping_file).to_dict('records')}
            data_reporting = pd.read_csv(data_reporting_file)
            data_outliers = pd.read_csv(data_outliers_file)
            data_std = pd.read_csv(data_std_file)
            data_iqr = pd.read_csv(data_iqr_file)
            indicator_group = pd.read_csv(indicator_group_file)
        # TODO Need to export the result of this to csvnas back up if next run fails, and print a warining message when this happens

    else:
        columns = {x.get('new'): x.get('old') for x in pd.read_csv(
            columns_mapping_file).to_dict('records')}
        data_reporting = pd.read_csv(data_reporting_file)
        data_outliers = pd.read_csv(data_outliers_file)
        data_std = pd.read_csv(data_std_file)
        data_iqr = pd.read_csv(data_iqr_file)
        indicator_group = pd.read_csv(indicator_group_file)

    return columns, data_reporting, data_outliers, data_std, data_iqr, indicator_group
