from store import timeit, reporting_count_transform, init_data_set
from package.layout.chart_card import ChartDataCard


@timeit
def bar_reporting_country_plot(data):

    data_in = data.get("reporting_country")
    data_out = reporting_count_transform(data_in.copy())

    return data_out


# DATACARD 5 #


stacked_bar_reporting_country = ChartDataCard(
    title="Reporting for $label$",
    data=init_data_set,
    data_transform=bar_reporting_country_plot,
    fig_title="Total number of facilities reporting on their 105:1 form and reported a positive number of $label$ in country",
    fig_object="Bar",
)

stacked_bar_reporting_country.set_colors(
    {"fig": ["rgb(42, 87, 131)", "rgb(247, 190, 178)", "rgb(211, 41, 61)"]}
)
