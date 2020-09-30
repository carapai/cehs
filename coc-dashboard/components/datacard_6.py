import pandas as pd
from package.layout.map_card import MapDataCard

from store import check_index, timeit, init_data_set, shapefile


@timeit
def map_reporting_dated_plot(data):

    data_in = data.get("reporting_dated")

    last_date = data_in.date.max()

    last_date_df = data_in[data_in.date == last_date]

    last_date_df = check_index(last_date_df)

    val_col = last_date_df.columns[0]

    last_date_df = last_date_df.reset_index()

    districts = []
    reporting = []
    for district in last_date_df.id.unique():
        districtal_df = last_date_df[last_date_df.id == district]
        total_facilities = (districtal_df[val_col] != "not_expected").sum()
        reported_facilities = len(
            districtal_df[districtal_df[val_col] == "positive_indic"]
        )
        report_rate = round((reported_facilities / total_facilities) * 100, 2)
        districts.append(district)
        reporting.append(report_rate)

    reporting_df = pd.DataFrame({"id": districts, "Reporting rate": reporting})
    reporting_df = reporting_df.set_index("id")

    data_out = {
        f"Reporting rate during {last_date.to_pydatetime().strftime('%B %Y')}": reporting_df
    }

    return data_out


# DATACARD 6 #

reporting_map = MapDataCard(
    data=init_data_set,
    data_transform=map_reporting_dated_plot,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
)
