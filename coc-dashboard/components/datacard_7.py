from store import reporting_count_transform, timeit, init_data_set
from package.layout.chart_card import ChartDataCard


@timeit
def scatter_reporting_district_plot(data):

    data_in = data.get("reporting_district")
    data_out = reporting_count_transform(data_in.copy())

    return data_out


# DATACARD 7 #


stacked_bar_district = ChartDataCard(
    data=init_data_set,
    data_transform=scatter_reporting_district_plot,
    fig_title="Total number of facilities reporting on their 105:1 form and reporting on $label$",
    fig_object="Bar",  # Relies on the 'overlay' layout barmode parameter for stacking
)

stacked_bar_district.set_colors(
    {"fig": ["rgb(42, 87, 131)", "rgb(247, 190, 178)", "rgb(211, 41, 61)"]}
)
