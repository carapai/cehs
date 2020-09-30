from store import init_data_set, get_sub_dfs, month_order, timeit
from model.grid import Grid
import numpy as np
import pandas as pd

# !FIXME

indicator_values = [
    "1st ANC Visits",
    "4th ANC Visits",
    "Maternity Admissions",
    "Deliveries in unit",
    "Deliveries in unit - live",
    "Deliveries in unit - fresh stillbirth",
    "Deliveries in unit - macerated stillbirth",
    "Newborn deaths",
    "Postnatal Visits",
    "Low weight births",
    "BCG",
    "DPT1",
    "DPT3",
    "HPV1",
    "HPV2",
    "MR1",
    "PCV1",
    "PCV3",
    "TD1",
    "TD2",
    "TD3",
    "TD4-5",
    "Malaria cases",
    "OPD attendance",
    "Malaria cases treated",
    "Malaria tests",
    "Mat tested HIV positive",
    "Mat tested HIV",
    "Malaria deaths",
    "ANC tested HIV",
    "ANC tested HIV positive",
    "ANC initiated on ART",
    "Tested HIV",
    "Tested HIV positive",
    "HIV positive linked to care",
    "Mat initiated on ART",
    "PNC tested HIV",
    "PNC tested HIV positive",
    "PNC initiated on ART",
    "IPD attendance",
    "TB cases registered",
    "Number of doses of vitamin A distributed",
    "Number of SAM admissions",
    "Number of MAM admissions",
]


@timeit
def get_sub_df_with_year(df, values):
    """
    Extract and return a dictionary of dictionaries splitting each original dictionary df entry into traces based on values
    """

    traces = {}
    # district_color_map = district_color_palette(df)
    for value in values:
        sub_df = df[["id", "year", value]]
        # sub_df['color'] = sub_df.id.map(lambda x: district_color_map.get(x))
        sub_df = (
            sub_df.groupby(
                by=[
                    "id",
                    "year",  #'color'
                ]
            )
            .sum()
            .reset_index()
        )
        traces[value] = sub_df

    return traces


@timeit
def bar_transform_multiple(data):

    data_in = data.get("indicator_group").reset_index()
    first_date = data_in.date.min().to_pydatetime()
    last_date = data_in.date.max().to_pydatetime()
    data_out = {}

    mask = (
        (data_in.year == first_date.year)
        & (data_in.month == month_order[first_date.month - 1])
    ) | (
        (data_in.year == last_date.year)
        & (data_in.month == month_order[last_date.month - 1])
    )

    data_in = data_in[mask]
    indicator_values = [
        x
        for x in data_in.columns
        if x
        not in ["index", "id", "year", "date", "month", "facility_id", "facility_name"]
    ]
    data_in = get_sub_df_with_year(data_in, indicator_values)
    for (name, data_input) in data_in.items():
        val_col = data_input.columns[-1]
        data_in = data_input.pivot_table(
            columns="year", values=val_col, index=["id"]
        )  # , 'color'])
        data_in[val_col] = (
            (data_in[last_date.year] - data_in[first_date.year])
            / data_in[first_date.year]
        ) * 100
        data_in[val_col] = data_in[val_col].apply(lambda x: round(x, 2))
        data_in = data_in[[val_col]].reset_index()
        data_in["id"] = data_in["id"].astype(str)
        data_in = data_in.set_index(["id"])  # , 'color'])
        data_in = data_in[~pd.isna(data_in[val_col])]
        # note some infinity values were created earlier on so we are going to turn thoese to nan
        data_in = data_in.replace([np.inf, -np.inf], np.nan)
        data_in = data_in.nlargest(10, val_col)

        if name in data_out:
            data_out[name].append(data_in)
        else:
            data_out[name] = data_in
        # print(data_out)
    return data_out


# for name, df in init_data_set.items():
#     print(name)
#     print(df.head())
#     print(df.columns)

grid = Grid(
    data=init_data_set,
    data_transform=bar_transform_multiple,
    title="Top 10 Districts that have seen the highest percentage change across all Indicators between target and reference date",
)
