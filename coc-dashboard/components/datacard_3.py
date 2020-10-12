import pandas as pd
from package.layout.chart_card import ChartDataCard

from store import get_sub_dfs, timeit, month_order, init_data_set


from package.layout.chart_card import ChartDataCard


@timeit
def scatter_district_plot(df):

    df_district = df.get("district")

    df_district = df_district[df_district[df_district.columns[0]] > 0]

    df_district = get_sub_dfs(
        df_district, "year", [2018, 2019, 2020], "month", month_order
    )

    return df_district


# DATACARD 3 #


district_overview_scatter = ChartDataCard(
    title="Deep-dive in the selected district: The number of $label$ changed by % between 05-2019 and 05-2020",
    fig_title="Total $label$ in the selected district",
    data=init_data_set,
    data_transform=scatter_district_plot,
    fig_type="Scatter",
)

district_overview_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        }
    }
)
