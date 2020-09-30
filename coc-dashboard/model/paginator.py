import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


class Paginator:
    def __init__(self):
        self.clicked = "Dashboard"
        self.highlighted_style = {"border": "3px solid red", "fontWeight": "bold"}
        self.default_style = {"border": "3px solid gray"}

    @property
    def layout(self):
        layout = html.Div(
            self.get_layout(),
            style={"position": "fixed", "top": "25px", "left": "20px"},
            id="paginator",
        )
        return layout

    def get_layout(self):
        return [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Dashboard",
                            className="mb-3",
                            id="dashboard-button",
                            style=self.highlighted_style
                            if self.clicked == "Dashboard"
                            else self.default_style,
                        )
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Reporting",
                            className="mb-3",
                            id="reporting-button",
                            style=self.highlighted_style
                            if self.clicked == "Reporting"
                            else self.default_style,
                        )
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Overview",
                            className="mb-3",
                            id="overview-button",
                            style=self.highlighted_style
                            if self.clicked == "Overview"
                            else self.default_style,
                        )
                    ),
                ]
            )
        ]

    def _requires_dropdown(self):
        return False
