import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# FIXME: For some reason this is not working (even if function is made not private, so I pasted in the functions here for now, but ideally they would be imported)
# from package.layout.data_story import __get_dropdown_layout, _requires_dropdown


class DataCard:

    default_colors = {'title': '#3c6792',
                      'subtitle': '#555555',
                      'text': '#363638',
                      'fig': ['#b00d3b', '#f77665', '#e2d5d1', '#96c0e0', '#3c6792']
                      }

    def __init__(self, data: {str: pd.DataFrame} = None, **kwargs):

        # self._dropdowns = kwargs.get('dropdowns')

        # Data
        self.data_transform = kwargs.get('data_transform')
        self.__data = {}
        self.data = data or {}

        # Content
        self.title = kwargs.get('title', '')
        self.figure_title = kwargs.get('fig_title', '')
        self.key_points = kwargs.get('key_points')

        # Style
        self.__colors = self.default_colors.copy()
        self.set_colors(kwargs.get('colors', self.default_colors.copy()))

        # Layout
        # Orientation
        self.orientation_left = kwargs.get(
            'orientation_left', True)
        self.orientation_vertical = kwargs.get(
            'orientation_vertical', False)

        # Private properties

        self.__figure = kwargs.get('figure')
        self.__layout = None
        self.__name = None

        # setting other keyword arguments
        for arg_name, arg_val in kwargs.items():
            setattr(self, arg_name, arg_val)

        # Housekeeping
        # self._data_columns = self._get_all_columns()
        self._data_columns = ['One'] # !FIXME

        # Callbacks

        self.callbacks = []
        # self.callbacks = [
        #     {'func': self.__update_figure,
        #      'input': [(f'{self.my_name}_dropdown', 'value')],
        #      'output': [(f'{self.my_name}_figure', 'figure'),
        #                 (f'{self.my_name}_fig_title', 'children')]
        #      }]


    @property
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, value):
        self.set_colors(value)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        assert type(value) == dict, \
               'Data should be dict with pandas DataFrame as values'
        self.__data = self.data_transform(value) \
                      if self.data_transform \
                      else value

    @property
    def figure(self):
        self.figure = self._get_figure(self._get_data())
        return self.__figure

    @figure.setter
    def figure(self, fig):
        assert type(
            fig) == go.Figure, 'Figure should be plotly Graph Object Figure'
        fig.update_layout(
            margin={'r': 0, 't': 20, 'l': 0, 'b': 20},
            coloraxis=dict(colorbar_len=1),
            showlegend=True,
        )
        self.__figure = fig

    @property
    def layout(self):
        self.__layout = self.__get_layout()
        return self.__layout

    @layout.setter
    def layout(self, value):
        self.__layout = value

    @ property
    def my_name(self):
        if self.__name is None:
            self.__name = str(self).split('>')[0][-11:]
        return self.__name

    @property
    def figure_title(self):
        return self._get_figure_title(self._get_data())

    @figure_title.setter
    def figure_title(self, fig_title):
        self.__figure_title = fig_title

    ##################
    #     LAYOUT     #
    ##################

    def _get_figure(self, data):
        raise NotImplementedError(
            'Every child method should implement _get_figure(self,data) method.')

    def __get_layout(self):
        '''Get the static plotly layout of a data card'''
        els = [self.__get_figure_layout() if self.data or self.figure else None,
               self.__get_text_layout(self.key_points) if self.key_points else None]

        layout = dbc.Col([
            dbc.Row(
                dbc.Col(
                    html.H3(self.__format_string(self.title, self.data),
                            style={'color': self.colors['title'],
                                   'text-align': 'center'},
                            className='w-100',
                            id=f'{self.my_name}_title'
                            ),
                    className='data-card__header-container'
                ) if self.title != '' else None
            ),
            *self.__get_orientation(els)], className="m-bot-24", id=f'{self.my_name}_layout')

        return layout

    ##    FIGURE    ##

    def _get_figure(self, data):
        raise NotImplementedError(
            'Every child method should implement _get_figure(self,data) method.')

    def __get_figure_layout(self):
        layout = dbc.Col(
            [
                dbc.Row(
                    self.__get_figure_title_layout()
                ),
                # dbc.Row(
                #     self.__get_dropdown_layout(),
                #     className='dropdown-section'
                # ),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=self.figure,
                                  config={'displayModeBar': False},
                                  id=f'{self.my_name}_figure')
                    )
                )
            ],
        )
        return layout

    ## FIGURE TITLE ##

    def _get_figure_title(self, data):
        formated_fig_title = self.__format_string(self.__figure_title, data)

        fig_title = html.H5(html.B(formated_fig_title),
                            style={'color': self.colors['subtitle'],
                                   'text-align': 'center',
                                   'width': '100%'
                                   }
                            )

        return fig_title

    def __get_figure_title_layout(self):

        figure_title_layout = dbc.Col(
            self.figure_title,
            align='center',
            style={'text-align': 'center'},
            id=f'{self.my_name}_fig_title'
        )

        return figure_title_layout

    ## DROPDOWN ##

    def __get_dropdown_layout(self):
        # TODO: Align dropdown with text
        # TODO: deal with passing the data to data card even when the figure is generic

        dropdown_layout = None
        if self._requires_dropdown():
            dropdown_layout = dbc.Col([
                html.Div(
                    html.P("Please select a metric:",
                           className='text-center m-0 p-0'),
                    style={'color': self.colors['text']}),
                html.Div(
                    dcc.Dropdown(id=f'{self.my_name}_dropdown',
                                 options=[{'label': x, 'value': x}
                                          for x in self._data_columns],
                                 # TODO: This needs to be updated to accept regions names!
                                 value=self._data_columns[0],
                                 clearable=False
                                 )
                )
            ])

        return dropdown_layout

    def _requires_dropdown(self):
        return False
        # return len(self._dropdowns) > 1 if self._dropdowns else False

    ## ORIENTATION ##

    def __get_orientation(self, els):
        els = els if self.orientation_left else els[::-1]
        return [dbc.Row(e) for e in els] if self.orientation_vertical else [dbc.Row(els)]

    ## TEXT SECTION ##

    def __get_text_layout(self, text):
        text_section_layout = dbc.Col([
            dbc.Row(
                dbc.Col(html.Div([self.__unwrap_section_and_points(section, points)
                                  for section, points in text.items()],
                                 className='h-90 w-75 text-section'
                                 )
                        )
            )
        ],
        )

        return text_section_layout

    def __unwrap_section_and_points(self, section, points):
        layout = html.Div([
            html.Div(html.H5(self.__format_string(section, self.data), style={
                     'color': self.colors['subtitle']})),
            html.Div(
                html.Ul([html.Li(html.P(self.__format_string(item, self.data))) for item in points]),
                        style = {'color': self.colors['text']})])
        return layout

    ###############
    #    STYLE    #
    ###############

    def set_colors(self, new_colors):
        for key, value in new_colors.items():
            if key == 'fig':
                figure_colors = new_colors.get('fig')
                self.__colors['fig'] = figure_colors \
                    if type(figure_colors) == dict \
                    else self.__get_dict_colors_from_list(figure_colors)
            else:
                self.__colors[key] = value

    def __get_dict_colors_from_list(self, color_list):
        colors_dict = {}
        if self.data:
            if len(self.data) > 1:
                colors_dict = dict(zip(self.data, color_list))
            else:
                if len(color_list) < 2:
                    color_list.insert(0, '#e2d5d1')
                colors_dict = {next(iter(self.data.keys())):
                               px.colors.make_colorscale(color_list)}
        return colors_dict

    #################
    #    HELPERS    #
    #################

    def __format_string(self, string, data):
        formatted_string = string
        if '$' in string:

            assert data != {}, 'Data has to be defined for labels to be dynamic'

            keys = {
                '$label$': next(iter(data.values())).columns[0]
            }

            # first, get rid of static replacements (first column names etc)
            for key, value in keys.items():
                formatted_string = formatted_string.replace(key, str(value))

            # deal with complex labels
            while '$' in formatted_string:
                sub = self.__get_substring_between_elements(
                    formatted_string, '$')

                try:
                    if 'trace' in sub:
                        trace_index = sub.split('.')[1]
                        formatted_string = formatted_string.replace(f'$trace.{trace_index}$',
                                                                    f'{list(data.keys())[int(trace_index)]}')

                    if 'data' in sub:
                        _, index, aggregation = sub.split('.')
                        func = getattr(np, aggregation)
                        formatted_string = formatted_string.replace(f'$data.{index}.{aggregation}$',
                                                                    f'{func(list(data.values())[int(index)])[0]}')

                except Exception as e:  # !TODO handle errors explicitly
                    print(e)
                    print(
                        'Dynamic string parsing error. Are you passing all necessary arguments?')
                    return formatted_string

        return formatted_string

    def __get_substring_between_elements(self, string, element, closing_element='$'):
        try:
            out = string.split(element, 1)[1]
            out = out.split(closing_element, 1)[0] \
                if closing_element in out \
                else None
        except IndexError as e:
            out = None
            print(e)
            print('All dynamic strings should have closing $ sign')
        return out

    def _get_data(self, data_column_name=None):
        if self.data == {}:
            return {}
        # Get the data column
        if not data_column_name:
            data_column_name = next(iter(self.data.values())).columns[0]
        # Get the datacolumn of each dataframe if the column exists
        # make sure that you are passing data frame, because label depends on a column name
        column_data = {name: data[[data_column_name]]
                       for name, data in self.data.items()
                       if data_column_name in data.columns}
        return column_data

    def _get_all_columns(self):
        # Get the data columns of all dataframes
        all_columns = set()
        for df in self.data.values():
            all_columns.update(list(df.columns))
        return list(all_columns)

    def _requires_dropdown(self):
        return len(self._get_all_columns()) > 1

    def __update_figure(self, value):
        '''Update the map and the map title to display the data corresponding to selected variable'''
        print(f'{self.my_name} firing a callback')
        data_dict = self._get_data(value)
        self.figure = self._get_figure(data_dict)
        self.figure_title = self._get_figure_title(data_dict)
        return [self.figure, self.figure_title]
