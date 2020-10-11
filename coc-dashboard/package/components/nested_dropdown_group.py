import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
from package.elements.nested_dropdown import NestedDropdown
from store import timeit


class NestedDropdownGroup:
    def __init__(self, dataframe, title=None, vertical=True):
        try:
            for col in dataframe.columns:
                dataframe[col] = dataframe[col].astype(str)
        except Exception as e:
            print(e)
            print("Error casting dropdown options to string type")
        self.dataframe = dataframe
        self.dropdowns = {}
        self.title = title
        self.vertical = vertical
        self.define_dropdowns()

        self.callbacks = [
            {
                "func": self.update_dropdown_options,
                "input": [(x, "value"), (x, "id"), (y, "id")],
                "output": [(y, "options")],
            }
            for (x, y) in zip(self.dropdown_ids[:-1], self.dropdown_ids[1:])
        ]

    @property
    def dropdown_ids(self):
        return list(self.dropdowns.keys())

    @property
    def dropdown_objects(self):
        return list(self.dropdowns.values())

    def get_current_values(self):
        return [x.value for x in self.dropdown_objects]

    def define_dropdowns(self):
        parent = None
        for name in self.dataframe.columns:
            # define dropdown options
            dropdown = NestedDropdown(
                id=name,
                options=self.dataframe[name].unique().tolist(),
                visible_id=False,
                clearable=False,
            )

            if parent:
                parent_dropdown = self.dropdowns.get(parent)
                parent_dropdown.add_child(dropdown)

            self.dropdowns[name] = dropdown

            parent = name

    @property
    def layout(self):
        layout = dbc.Col(
            [
                dbc.Row(
                    html.P(
                        self.title,
                        className="text-center",
                        style={
                            "border-bottom": "0.5px solid gray",
                            "font-weidht": "bold",
                            "width": "100%",
                        },
                    )
                )
                if self.title
                else None
            ]
            + self.get_orientation(self.dropdown_objects,
                                   vertical=self.vertical),
            className="p-3 m-12",
        )
        return layout

    def _requires_dropdown(self):
        return True

    def get_orientation(self, elements, vertical=True):
        elements = [e.get_layout() for e in elements]
        layout = [dbc.Row(e) for e in elements] if vertical else [
            dbc.Row(elements)]
        return layout

    @timeit
    def update_dropdown_options(self, *inputs):
        value = inputs[0]
        column = inputs[1]
        child_column = inputs[2]
        filtered_df = self.dataframe[self.dataframe[column] == value]
        options = filtered_df[child_column].unique().tolist()
        dropdown_options = [{"label": x, "value": x} for x in options]
        return [dropdown_options]

    def attach_tail_to_callback(self, func, output):
        """Attach callback to the tail element of this dropdown group

        DBC: Given valid function that takes in value and id of dropdown and
        returns updated property of specified element, attach the callback to be registered by dashboard class.

        Args:
            func (function): Transformation function that should be executed upon the firing of the callback
            output ([(id, property)]): Id and property of updated element
        """

        self.callbacks.append(
            {
                "func": func,
                "output": output,
                "input": [
                    (self.dropdown_ids[-1], "value"),
                    (self.dropdown_ids[-1], "id"),
                ],
            }
        )
