import numpy as np
import pandas as pd
from store import check_index, timeit, get_sub_dfs, init_data_set, month_order
from package.layout.area_card import AreaDataCard
from package.layout.chart_card import ChartDataCard


@timeit
def tree_map_district_dated_plot(data):

    data_in = data.get("district_dated")
    data_in = check_index(data_in)
    val_col = data_in.columns[0]
    data_in[val_col] = data_in[val_col].apply(lambda x: int(x) if pd.notna(x) else 0)
    data_in = data_in.reset_index()
    data_in = data_in[data_in.date == data_in.date.max()].reset_index()
    district_name = data_in.id[0]
    data_tree = data_in.pivot_table(
        values=val_col, index=["facility_name"], columns="date", aggfunc=np.sum
    )
    data_out = {district_name: data_tree}
    return data_out


@timeit
def scatter_facility_plot(data):
    data = data.get("facility")

    data = check_index(data)
    data = data[data[data.columns[0]] > 0]
    data = get_sub_dfs(data, "year", [2018, 2019, 2020], "month", month_order)

    return data


tree_map_district = AreaDataCard(
    title="The contribution of individual facilities in the selected district",
    data=init_data_set,
    data_transform=tree_map_district_dated_plot,
    fig_object="Treemap",
)
tree_map_district.set_colors({"fig": ["#e2d5d1", "#96c0e0", "#3c6792"]})


facility_scatter = ChartDataCard(
    fig_title="Evolution of $label$ (click on the graph above to filter)",
    data=init_data_set,
    data_transform=scatter_facility_plot,
)

facility_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        }
    }
)
