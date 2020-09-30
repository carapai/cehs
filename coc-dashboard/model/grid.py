import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np


class Grid:
    """
    Define the grid layout for all the charts.
    """

    def __init__(self, data, **kwargs):
        self.title = kwargs.get("title", None)
        self.data_transform = kwargs.get("data_transform")

        self.__data = None
        self.data = data
        self.__name = None

        self.callbacks = []

    @property
    def layout(self):
        layout = [
            dbc.Row(
                dbc.Col(
                    html.H3(
                        self.__format_string(self.title, self.data),
                        style={"color": "#3c6792", "text-align": "center"},
                        className="w-100",
                        id=f"{self.my_name}_title",
                    ),
                    className="data-card__header-container",
                )
                if self.title != ""
                else None
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                dbc.Col(
                                    name,
                                    align="center",
                                    className="m-top-24",
                                    style={"text-align": "center"},
                                    id=f"{name}_fig_title",
                                )
                            ),
                            self.create_fig(name, x),
                        ],
                        width=4,
                    )
                    for (name, x) in self.data.items()
                ],
                className="m-top-24",
            ),
        ]
        return dbc.Col(layout)

    def create_fig(self, name, data):
        """
        Creates a single bar chart
        """
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                y=data.index,
                x=data[data.columns[0]],
                marker=dict(reversescale=True),
            )
        )
        fig.update_traces(textposition="inside", orientation="h", showlegend=False)
        # fig['layout']['xaxis']['autorange'] = "reversed"
        fig["layout"]["yaxis"]["autorange"] = "reversed"
        fig.update_layout(margin={"r": 0, "t": 20, "l": 0, "b": 20})
        return dcc.Graph(figure=fig, id=name, config={"displayModeBar": False})

    def _requires_dropdown(self):
        return True

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        assert (
            type(value) == dict
        ), "Data should be dict with pandas DataFrame as values"
        self.__data = self.data_transform(value) if self.data_transform else value

    @property
    def my_name(self):
        if self.__name is None:
            self.__name = str(self).split(">")[0][-11:]
        return self.__name

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
