import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


class Methodology:
    def __init__(self, elements):

        self.elements = elements
        self.callbacks = []

    @property
    def layout(self):
        el_layout = [dbc.Row(x.layout) for x in self.elements]

        layout = html.Div(
            [
                dbc.Button(
                    "Show Info",
                    id="fade-button2",
                    className="mb-3",
                    style={"position": "fixed", "right": "20px", "top": "20px"},
                ),
                dbc.Fade(
                    el_layout,
                    id="fade2",
                    is_in=False,
                    style={
                        "transition": "opacity 100ms ease",
                        "background": "white",
                        "height": "auto",
                        "width": "30vw",
                        "overflow": "visible",
                        "position": "fixed",
                        "right": "20px",
                        "top": "80px",
                    },
                    className="top shadow-sm p-3 mb-5 rounded",
                ),
            ],
            className="top",
        )
        return layout

    def _requires_dropdown(self):
        return False
