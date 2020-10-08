import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd


def read_data(engine, test=False):

    columns_mapping_file = "./coc-dashboard/data/columns.csv"
    data_outliers_file = "./coc-dashboard/data/outlier_data.csv"
    data_reporting_file = "./coc-dashboard/data/report_data.csv"
    data_std_file = "./coc-dashboard/data/std_no_outlier_data.csv"
    data_iqr_file = "./coc-dashboard/data/iqr_no_outlier_data.csv"
    indicator_group_file = "./coc-dashboard/data/groups.csv"

    # TODO delete references to test
    if test == False:
        try:
            columns = {
                x.get("old"): x.get("new")
                for x in pd.read_sql(
                    "SELECT new, old FROM columns_index;", con=engine
                ).to_dict("records")
            }

            data_reporting = pd.read_sql(
                """SELECT reporting.*, facilities_index.facility_name
                                            FROM reporting
                                            JOIN facilities_index
                                            ON reporting.facility_id = facilities_index.facility_id""",
                con=engine,
            )

            data_outliers = pd.read_sql(
                """SELECT with_outliers.*, facilities_index.facility_name
                                        FROM with_outliers
                                        JOIN facilities_index
                                        ON with_outliers.facility_id = facilities_index.facility_id""",
                con=engine,
            )

            data_std = pd.read_sql(
                """SELECT no_outliers_std.*, facilities_index.facility_name
                                    FROM no_outliers_std
                                    JOIN facilities_index
                                    ON no_outliers_std.facility_id = facilities_index.facility_id""",
                con=engine,
            )

            data_iqr = pd.read_sql(
                """SELECT no_outliers_iqr.*, facilities_index.facility_name
                                    FROM no_outliers_iqr
                                    JOIN facilities_index
                                    ON no_outliers_iqr.facility_id = facilities_index.facility_id""",
                con=engine,
            )
            indicator_group = pd.read_sql(
                "SELECT * FROM indicator_groups_new", con=engine
            )
        except Exception as e:
            print(e)
            columns = {
                x.get("new"): x.get("old")
                for x in pd.read_csv(columns_mapping_file)[['old', 'new']].to_dict("records")
            }
            data_reporting = pd.read_csv(data_reporting_file)
            data_outliers = pd.read_csv(data_outliers_file)
            data_std = pd.read_csv(data_std_file)
            data_iqr = pd.read_csv(data_iqr_file)
            indicator_group = pd.read_csv(indicator_group_file)

        # TODO Need to export the result of this to csv back up if next run fails, and print a warning message when this happens

    else:
        columns = {
            x.get("old"): x.get("new")
            for x in pd.read_csv(columns_mapping_file)[['old', 'new']].to_dict("records")
        }
        data_reporting = pd.read_csv(data_reporting_file)
        data_outliers = pd.read_csv(data_outliers_file)
        data_std = pd.read_csv(data_std_file)
        data_iqr = pd.read_csv(data_iqr_file)
        indicator_group = pd.read_csv(indicator_group_file)

    data_reporting = data_reporting.rename(columns=columns)
    data_outliers = data_outliers.rename(columns=columns)
    data_std = data_std.rename(columns=columns)
    data_iqr = data_iqr.rename(columns=columns)

    return columns, data_reporting, data_outliers, data_std, data_iqr, indicator_group
