import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import Dash
from flask import send_from_directory
from package import here
from package.layout.base.dashboard import Dashboard
from package.layout.base.data_card import DataCard
from store import timeit


class DataStory(Dashboard):
    # (self, data_sets:{}, data_cards:[]=None, **kwargs)
    def __init__(self, data_cards: [] = None, **kwargs):
        # TODO: **kwargs loop for any remaining kwargs?
        super(DataStory, self).__init__(**kwargs)
        self.__name = None
        self._dropdowns = kwargs.get("dropdowns")
        self.data_cards = data_cards
        self.title = kwargs.get("title", "")
        self.sub_title = kwargs.get("sub_title", "")
        self.text_section = kwargs.get("text_section", "")
        self.footer_image = kwargs.get("footer_image", None)
        self.footer_text = kwargs.get("footer_text", None)
        self.ind_elements = kwargs.get("ind_elements", [])  # FIXME

    @property
    def my_name(self):
        if self.__name is None:
            self.__name = str(self).split(">")[0][-11:]
        return self.__name

    @timeit
    def get_layout(self):

        layout = (
            [self.__get_header()]
            + [
                dbc.Row(
                    x.layout, className="data-card shadow-sm p-3 mb-5 rounded m-top-24"
                )
                for x in self.data_cards
            ]
            + [self.__get_footer()]
        )

        return layout

    @timeit
    def get_container(self):
        return dbc.Container(self.get_layout(), id="ds-container")

    def _set_layout(self):
        layout = html.Div(
            [
                html.Div(
                    [
                        html.Link(rel="stylesheet", href="/static/css/data_story.css"),
                        html.Link(
                            href="https://fonts.googleapis.com/css2?family=Lato&display=swap",
                            rel="stylesheet",
                        ),
                        html.Link(
                            href="https://fonts.googleapis.com/icon?family=Material+Icons",
                            rel="stylesheet",
                        ),
                        dcc.Location(id="url", refresh=False),
                    ],
                    id="meta",
                ),
                html.Div(
                    [el.layout for el in self.ind_elements], id="independent-elements"
                ),
                html.Div(self.get_container(), id="ds-paginator"),
            ],
            id="ds-wrapper",
        )

        self.app.layout = layout

    def __get_header(self):
        header_layout = dbc.Row(
            dbc.Col(
                [
                    dbc.Row(
                        dbc.Col(
                            html.Img(
                                src="/static/images/UNICEF-MOH-header-resized.jpg",  # TODO automatic placement
                                className="ds-header__logo m-top-24",
                            )
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            [
                                html.Div(
                                    html.H1(self.title, className="text-center"),
                                    className="color-primary-dark",
                                ),
                                html.Div(
                                    html.H3(self.sub_title, className="text-center"),
                                    className="color-secondary-dark",
                                ),
                            ]
                        ),
                        className="ds-header-container m-24",
                    ),
                    dbc.Row(
                        dbc.Col(
                            html.H5(self.text_section, className="text-center"),
                            className="color-secondary-dark",
                        )
                    ),
                ],
                className="header",
            )
        )

        return header_layout

    def __get_footer(self):

        footer_layout = [
            dbc.Row(
                dbc.Col(
                    html.Img(
                        src=self.footer_image,
                        style={"width": "100%"},
                        className="ds-header__logo m-top-24",
                    )
                )
                if self.footer_image
                else None
            ),
            dbc.Row(
                dbc.Col(html.H6(self.footer_text, className="text-right m-12"))
                if self.footer_text
                else None
            ),
        ]

        return dbc.Row(dbc.Col(footer_layout))
