import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash_bootstrap_components.themes import BOOTSTRAP
from dash.dependencies import Input, Output
import pandas as pd


class NestedDropdown:
    def __init__(self, id, options, **kwargs):
        self.id = id
        self.options = self.list_to_options(options)
        self.__value = None
        self.value = kwargs.pop("value", options[0])

        self.parents = []
        self.children = []
        self.visible_id = kwargs.pop("visible_id", True)

        self.dropdown_settings = kwargs

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        try:
            self.__value = str(val)
        except Exception as e:
            print(e)
            print("Error casting value to string.")

    def list_to_options(self, options):
        return [{"value": x, "label": x} for x in options]

    def get_layout(self):
        self.set_layout(self.options, **self.dropdown_settings)
        return self.layout

    def set_layout(self, options, **kwargs):
        layout = [
            html.Div(
                html.P(self.id, className="text-center m-0 p-0"),
                style={"color": "#363638"},
            )
            if self.visible_id
            else None,
            dcc.Dropdown(
                options=options,
                id=self.id,
                value=self.value,
                persistence=True,
                persistence_type="session",
                className="m-1",
                **kwargs
            ),
        ]
        self.layout = dbc.Col(
            layout, style={"overflow": "visible !important"}, className="m-12"
        )

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
        if self not in child.parents:
            child.add_parent(self)

    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
        if self not in parent.children:
            parent.add_child(self)

    # def get_options(self, value=None):
    #     if self.filtered_by:
    #         self.options = self.dependency.get(value)
    #         if type(self.options) == dict:
    #             self.options = list(self.options.keys())
    #     return self.options
