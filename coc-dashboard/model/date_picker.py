import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


class DatePicker:
    def __init__(self, element_id, min_date, max_date, initial_visible_month=None):
        self.id = element_id
        self.min_date = min_date
        self.max_date = max_date
        self.initial_visible_month = initial_visible_month or self.min_date

    @property
    def layout(self):
        layout = dbc.Col(
            [
                html.Div(
                    html.P(self.id, className="text-center m-0 p-0"),
                    style={"color": "#363638"},
                ),
                dcc.DatePickerSingle(
                    id=self.id,
                    min_date_allowed=self.min_date,
                    max_date_allowed=self.max_date,
                    initial_visible_month=self.initial_visible_month,
                    persistence=True,
                    persistence_type="session",
                    style={"width": "100%"},
                ),
            ],
            style={"width": "100%"},
        )
        return layout


# !TODO style date pickers
class DatePickerGroup:
    def __init__(self, els: []):
        self.els = els
        self.callbacks = []

    @property
    def layout(self):
        return dbc.Col(dbc.Row([x.layout for x in self.els]))

    def _requires_dropdown(self):
        return False
