import pandas as pd
from model import CardLayout
from package.layout.chart_card import ChartDataCard
from package.layout.map_card import MapDataCard
from store import shapefile, init_data_set, timeit


@timeit
def map_country_dated_plot(data):

    data = data.get("dated")

    data_out = {f"Change between reference and target date": data}

    return data_out


@timeit
def bar_country_dated_plot(data):

    data = data.get("dated")

    data[data.columns[0]] = data[data.columns[0]] / 100

    data["rank"] = data.rank(ascending=True)
    data = data[data["rank"] < 11].sort_values(by="rank")
    data.drop("rank", axis=1, inplace=True)
    data_out = {"Top/Bottom 10": data}

    return data_out


# DATACARD 2 #


country_overview_map = MapDataCard(
    data=init_data_set,
    data_transform=map_country_dated_plot,
    geodata=shapefile,
    locations="id",
    map_tolerance=0.005,
)

bar_chart_ranks_bottom = ChartDataCard(
    data=init_data_set,
    data_transform=bar_country_dated_plot,
    fig_object="Bar",
    bar_mode="overlay",
)

country_overview = CardLayout(
    title="Percentage change of $label$ between target and reference date by district",
    elements=[country_overview_map, bar_chart_ranks_bottom],
)

# TODO Define common color scale for map and barchart
