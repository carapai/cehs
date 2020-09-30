import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from package.elements.nested_dropdown import NestedDropdown


class MethodologySection:
    def __init__(self, **kwargs):
        self.data = kwargs.get("data", "")
        self.title = kwargs.get("title", "")

    @property
    def layout(self):
        el_layout = [
            dbc.Row(
                dbc.Col(
                    [
                        html.Div(html.H6(html.B(x["sub_title"]))),
                        html.Div(html.H6(x["body"], style={"font-size": "14px"})),
                        html.Div(
                            [
                                html.Li(d, style={"font-size": "14px"})
                                for d in x["list_data"]
                            ]
                        ),
                    ]
                )
            )
            for x in self.data
        ]

        layout = [
            dbc.Row(
                dbc.Col(
                    html.Div(
                        html.H4(
                            html.B(self.title),
                            style={
                                "color": "#00000",
                                "text-align": "center",
                                "text-decoration": "underline",
                                "width": "100%",
                            },
                        )
                    )
                )
            )
        ] + el_layout

        return dbc.Col(layout)
