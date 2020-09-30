import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


class StatisticSummary:
    def __init__(self, data, **kwargs):
        self.statistic_data = data
        self.text_centered = "text-center m-24"
        self.card_one = "m-24-full card-district"
        self.card_two = "m-24-full card-facility"

    @property
    def layout(self):
        return dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5(
                                f'{self.statistic_data.get("facilities")} Facilities in {self.statistic_data.get("districts")} \
                                        Districts ',
                                className=self.text_centered,
                            ),
                            className=self.card_one,
                        ),
                        dbc.Col(
                            html.H5(
                                f'Showing data across {self.statistic_data.get("indicators")} Indicators',
                                className=self.text_centered,
                            ),
                            className=self.card_two,
                        ),
                        dbc.Col(
                            html.H5(
                                f"Years Represented in the data are 2020, 2019, 2018",
                                className=self.text_centered,
                            ),
                            className=self.card_one,
                        ),
                    ],
                    className="m-24-full",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5(
                                    f" Average No. of General OPD Visits in 2019",
                                    className=self.text_centered,
                                ),
                                html.H5(
                                    f'{self.statistic_data.get("avg_opd")}',
                                    className=self.text_centered,
                                ),
                            ],
                            className=self.card_one,
                        ),
                        dbc.Col(
                            [
                                html.H5(
                                    f" Average No. of Women who attended 1st ANC Visits in 2019",
                                    className=self.text_centered,
                                ),
                                html.H5(
                                    f'{self.statistic_data.get("avg_first_anc_women")}',
                                    className=self.text_centered,
                                ),
                            ],
                            className=self.card_two,
                        ),
                        dbc.Col(
                            [
                                html.H5(
                                    f"Average no. of children under one who received DPT3 in 2019",
                                    className=self.text_centered,
                                ),
                                html.H5(
                                    f'{self.statistic_data.get("avg_dpt3")}',
                                    className=self.text_centered,
                                ),
                            ],
                            className=self.card_one,
                        ),
                    ],
                    className="m-24-full",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5(
                                    f"Average No. of severe acute malnutrition (SAM) admissions in 2019",
                                    className=self.text_centered,
                                ),
                                html.H5(
                                    f'{self.statistic_data.get("avg_sam")}',
                                    className=self.text_centered,
                                ),
                            ],
                            className=self.card_one,
                        ),
                        dbc.Col(
                            [
                                html.H5(
                                    f"Average No. of individuals diagnosed with Malaria in 2019",
                                    className=self.text_centered,
                                ),
                                html.H5(
                                    f'{self.statistic_data.get("avg_malaria_cases")}',
                                    className=self.text_centered,
                                ),
                            ],
                            className=self.card_two,
                        ),
                        dbc.Col(
                            [
                                html.H5(
                                    f"Average No. of TB cases registered in 2019",
                                    className=self.text_centered,
                                ),
                                html.H5(
                                    f'{self.statistic_data.get("avg_tb")}',
                                    className=self.text_centered,
                                ),
                            ],
                            className=self.card_one,
                        ),
                    ],
                    className="m-24-full",
                ),
                dbc.Row(
                    [
                        dbc.Col(),
                        dbc.Col(
                            [
                                html.H5(
                                    f"Average No. of Individuals who Tested HIV Positive in 2019",
                                    className=self.text_centered,
                                ),
                                html.H5(
                                    f'{self.statistic_data.get("avg_tested_hiv_positive")}',
                                    className=self.text_centered,
                                ),
                            ],
                            className=self.card_two,
                        ),
                        dbc.Col(),
                    ],
                    className="m-24-full",
                ),
            ]
        )

    def _requires_dropdown(self):
        return False
