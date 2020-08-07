import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import Dash
from flask import send_from_directory
from package import here
from package.layout.base.dashboard import Dashboard
from package.layout.base.data_card import DataCard


class DataStory(Dashboard):
    def __init__(self, data_cards: [] = None, **kwargs):  #(self, data_sets:{}, data_cards:[]=None, **kwargs)
        # TODO: **kwargs loop for any remaining kwargs?
        super(DataStory, self).__init__(**kwargs)
        self.__name = None
        self._dropdowns = kwargs.get('dropdowns')
        self.data_cards = data_cards
        self.title = kwargs.get('title', '')
        self.sub_title = kwargs.get('sub_title', '')
        self.text_section = kwargs.get('text_section', '')
        self.footer_image = kwargs.get('footer_image', None)
        self.footer_text = kwargs.get('footer_text', None)
        self.ind_elements = kwargs.get('ind_elements', []) # FIXME

    @ property
    def my_name(self):
        if self.__name is None:
            self.__name = str(self).split('>')[0][-11:]
        return self.__name


    def get_layout(self):

        layout = [self.__get_header()] + \
                [dbc.Row(x.layout, className='data-card shadow-sm p-3 mb-5 rounded m-top-24') \
                for x in self.data_cards] + \
                [self.__get_footer()] + \
                [el.layout for el in self.ind_elements]

        return layout

    def _set_layout(self):
        layout = html.Div([
                    html.Div([
                        html.Link(rel='stylesheet', href='/static/css/data_story.css'),
                        html.Link(href="https://fonts.googleapis.com/css2?family=Lato&display=swap",
                                  rel="stylesheet")
                        ]),
            dbc.Container(self.get_layout(),
                          id='ds-container')],
                id='ds-wrapper')

        self.app.layout = layout

    # def __get_dropdown_layout(self):
    #     # TODO: Align dropdown with text
    #     # TODO: Deal with passing the data to data card even when the figure is generic

    #     dropdowns_layout = None
    #     if self._requires_dropdown():
    #         dropdowns = []
    #         for dropdown_values_type, dropdown_values in self._dropdowns.items():
    #             # Create the layout
    #             dropdown_layout = dbc.Col([
    #                 html.Div(
    #                     # TODO: Make more flexible
    #                     html.P(f"Please select the {dropdown_values_type}"),
    #                     className='text-center m-0 p-0'),
    #                 html.Div(
    #                     dcc.Dropdown(id=f'{self.my_name}_{dropdown_values_type}_dropdown',
    #                                  options=[{'label': x, 'value': x}
    #                                           for x in dropdown_values],
    #                                  value=dropdown_values[0],
    #                                  clearable=False
    #                                  )
    #                 )
    #             ])
    #             dropdowns.append(dropdown_layout)

    #         dropdowns_layout = dbc.Col([dbc.Row(dropdown)
    #                                     for dropdown in dropdowns])

    #     return dropdowns_layout

    # def _requires_dropdown(self):
    #     return len(self._dropdowns) > 1 if self._dropdowns else False

    def __get_header(self):
        header_layout = dbc.Row(
            dbc.Col([
                dbc.Row(
                    dbc.Col(
                        html.Img(src='/static/images/UNICEF-MOH-header-resized.jpg',  # TODO automatic placement
                                     className='ds-header__logo m-top-24')
                    )
                ),
                dbc.Row(
                    dbc.Col([
                        html.Div(
                            html.H1(self.title, className='text-center'),
                            className='color-primary-dark'
                        ),
                        html.Div(
                            html.H3(self.sub_title, className='text-center'),
                            className='color-secondary-dark'
                        )
                    ]),
                    className='ds-header-container m-24'
                ),
                dbc.Row(
                    dbc.Col(
                        html.H5(self.text_section, className='text-center'),
                        className='color-secondary-dark'
                    )
                ),
            ], className='header'))

        return header_layout

    def __get_footer(self):
        footer_layout = dbc.Row(
            [
                dbc.Col(
                    html.H5(self.footer_text, className='text-right m-24')
                ) if self.footer_text else None,
                dbc.Col(
                    html.Img(src=self.footer_image,
                             style={'width': '100%'},
                             className='m-bot-24')
                ) if self.footer_image else None
            ]
        )

        return footer_layout
