import pandas as pd
from package.layout.chart_card import ChartDataCard

from store import get_sub_dfs, timeit, month_order, init_data_set


@timeit
def scatter_country_plot(df):

    df_country = df.get("country")

    df_country = df_country[df_country[df_country.columns[0]] > 0]

    df_country = get_sub_dfs(
        df_country, "year", [2018, 2019, 2020], "month", month_order
    )

    return df_country


# DATACARD 1 #


country_overview_scatter = ChartDataCard(
    title="Overview: Across the country, the number of $label$ changed by between 04-2019 and 04-2020",
    fig_title="Total $label$ across the country",
    data=init_data_set,
    data_transform=scatter_country_plot,
    fig_type="Scatter",
)

country_overview_scatter.set_colors(
    {
        "fig": {
            2018: "rgb(185, 221, 241)",
            2019: "rgb(106, 155, 195)",
            2020: "rgb(200, 19, 60)",
        }
    }
)
