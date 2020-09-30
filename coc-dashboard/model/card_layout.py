import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np


class CardLayout:
    default_colors = {
        "title": "#3c6792",
        "subtitle": "#555555",
        "text": "#363638",
        "fig": ["#b00d3b", "#f77665", "#e2d5d1", "#96c0e0", "#3c6792"],
    }

    def __init__(self, elements: [], **kwargs):
        self.els = elements
        self.title = kwargs.get("title", "")
        self.column_width = []

        self.__callbacks = []
        for x in self.els:
            self.__callbacks.extend(x.callbacks)

    @property
    def layout(self):
        layout = [
            dbc.Row(
                dbc.Col(
                    [
                        html.Div(
                            html.H5(
                                html.B(self.__format_string(self.title, self.data)),
                                style={
                                    "color": "#555555",
                                    "text-align": "center",
                                    "width": "100%",
                                },
                            )
                        )
                        if self.title != ""
                        else None
                    ]
                )
            ),
            dbc.Row(
                [
                    dbc.Col(self.els[0].layout, className="m-24", width=7),
                    dbc.Col(self.els[1].layout, className="m-24", width=5),
                ]
            ),
        ]
        # layout = [dbc.Col(x.layout, className='m-24') for x in self.els]
        return dbc.Col(layout)

    @property
    def data(self):
        return self.els[0].data

    @data.setter
    def data(self, value):
        for el in self.els:
            el.data = value

    @property
    def callbacks(self):
        return self.__callbacks

    def _requires_dropdown(self):
        return True

    def __format_string(self, string, data):
        formatted_string = string
        if "$" in string:

            assert data != {}, "Data has to be defined for labels to be dynamic"

            keys = {"$label$": next(iter(data.values())).columns[0]}

            # first, get rid of static replacements (first column names etc)
            for key, value in keys.items():
                formatted_string = formatted_string.replace(key, str(value))

            # deal with complex labels
            while "$" in formatted_string:
                sub = self.__get_substring_between_elements(formatted_string, "$")

                try:
                    if "trace" in sub:
                        trace_index = sub.split(".")[1]
                        formatted_string = formatted_string.replace(
                            f"$trace.{trace_index}$",
                            f"{list(data.keys())[int(trace_index)]}",
                        )

                    if "data" in sub:
                        _, index, aggregation = sub.split(".")
                        func = getattr(np, aggregation)
                        formatted_string = formatted_string.replace(
                            f"$data.{index}.{aggregation}$",
                            f"{func(list(data.values())[int(index)])[0]}",
                        )

                except Exception as e:  # !TODO handle errors explicitly
                    print(e)
                    print(
                        "Dynamic string parsing error. Are you passing all necessary arguments?"
                    )
                    return formatted_string

        return formatted_string

    def __get_substring_between_elements(self, string, element, closing_element="$"):
        try:
            out = string.split(element, 1)[1]
            out = out.split(closing_element, 1)[0] if closing_element in out else None
        except IndexError as e:
            out = None
            print(e)
            print("All dynamic strings should have closing $ sign")
