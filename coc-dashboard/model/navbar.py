import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


class Navbar:
    def __init__(self, elements, methodology=None):
        self.elements = elements
        self.active = "trends"
        self.methodology = methodology or []
        self.callbacks = []

        for els in elements:
            self.callbacks.extend(els.callbacks)

    @property
    def layout(self):
        layout = html.Div(self.get_layout(), id="topnav-container")

        return layout

    def get_nav_buttons(self, active="trends"):
        self.active = active

        active_style = "nav-element active"

        buttons = [
            html.P(
                "Trends",
                id="trends",
                className=active_style if active == "trends" else "nav-element",
            ),
            html.P(
                "Reporting",
                id="reporting",
                className=active_style if active == "reporting" else "nav-element",
            ),
            html.P(
                "Overview",
                id="overview",
                # active_style if active == "overview" else "nav-element",
                className="nav-element disabled",
            ),
        ]

        return buttons

    def get_layout(self):
        el_layout = [
            dbc.Row(x.layout, style={"margin": "0"}) for x in self.elements]
        me_layout = [dbc.Row(x.layout) for x in self.methodology]

        html_nav = html.Div(
            [
                html.Div(
                    self.get_nav_buttons(), className="topnav-left", id="nav-buttons"
                ),
                html.Div(
                    [
                        dbc.Button("Controls", id="fade-button"),
                        html.P(
                            html.Span("cloud_download",
                                      className="material-icons"),
                            className="nav-element",
                        ),
                        html.P(
                            html.Span("info", className="material-icons"),
                            # html.I(className="fas fa-info-circle"),
                            className="nav-element",
                            id="info-button",
                        ),
                    ],
                    className="topnav-right",
                ),
                dbc.Fade(
                    el_layout,
                    id="fade-controls",
                    is_in=False,
                    style={
                        "position": "fixed",
                        "top": "4em",
                        "right": "2em",
                        "transition": "opacity 100ms ease",
                        "background": "white",
                        "width": "25vw",
                        "overflow": "visible",
                    },
                    className="shadow-sm",
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Methodology"),
                        dbc.ModalBody(me_layout),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="info-close",
                                       className="ml-auto")
                        ),
                    ],
                    id="info-fade",
                    centered=True,
                ),
            ],
            className="topnav",
        )

        return html_nav

    def _requires_dropdown(self):
        return True
