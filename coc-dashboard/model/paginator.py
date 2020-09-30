import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


class Paginator:
    def __init__(self):
        self.clicked = "Dashboard"

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
                            style={"border": "3px solid red", "font-weight": "bold"}
                            if self.clicked == "Dashboard"
                            else {"border": "3px solid gray"},
                        )
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Reporting",
                            className="mb-3",
                            id="reporting-button",
                            style={"border": "3px solid red", "font-weight": "bold"}
                            if self.clicked == "Reporting"
                            else {"border": "3px solid gray"},
                        )
                    )
                ]
            )
        ]

    def _requires_dropdown(self):
        return False
