import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


class SideNav:
    def __init__(self, elements):

        self.elements = elements
        self.callbacks = []
        for els in elements:
            self.callbacks.extend(els.callbacks)

    @property
    def layout(self):
        el_layout = [dbc.Row(x.layout) for x in self.elements]

        layout = html.Div(
            [
                dbc.Button("Controls", id="fade-button", className="mb-3"),
                dbc.Fade(
                    el_layout,
                    id="fade",
                    is_in=False,
                    style={
                        "transition": "opacity 100ms ease",
                        "background": "white",
                        #    'padding': '12px 12px 12px 12px',
                        #    'border': '1px solid gray',
                        #    'height': '80vh',
                        "width": "25vw",
                        "overflow": "visible",
                    },
                    className="top shadow-sm p-3 mb-5 rounded",
                ),
            ],
            style={"position": "fixed", "left": "20px", "top": "75px"},
            className="top",
        )
        return layout

    def _requires_dropdown(self):
        return True
