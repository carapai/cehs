import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


class Datadownload:
    def __init__(self):

        # self.elements = elements
        self.callbacks = []

    @property
    def layout(self):

        layout = html.Div(
            [
                html.A(
                    dbc.Button("Download data", className="mb-3", id="download"),
                    id="download-excel",
                    href="",
                    download="data.xlsx",
                    style={"position": "fixed", "right": "140px", "top": "20px"},
                ),
            ],
            className="top",
        )
        return layout

    def _requires_dropdown(self):
        return False
