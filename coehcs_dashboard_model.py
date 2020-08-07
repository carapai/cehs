
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


class SideNav:

    def __init__(self, elements):

        self.elements = elements
        self.callbacks = []
        for els in elements:
            self.callbacks.extend(els.callbacks)

    @property
    def layout(self):
        el_layout = [dbc.Row(x.layout) for x in self.elements]

        layout = html.Div([
            dbc.Button("Hide controls", id="fade-button", className="mb-3"),
            dbc.Fade(
                el_layout,
                id="fade",
                is_in=True,
                style={'transition': 'opacity 100ms ease',
                       'background': 'white',
                    #    'padding': '12px 12px 12px 12px',
                    #    'border': '1px solid gray',
                    #    'height': '80vh',
                       'width': '25vw',
                       'overflow': 'visible'},
                className='top shadow-sm p-3 mb-5 rounded'
            )
        ], style={'position': 'fixed', 'left': '20px', 'top': '20px'}, className='top')
        return layout

    def _requires_dropdown(self):
        return True

class DatePicker:

    def __init__(self, element_id, min_date, max_date, initial_visible_month=None):
        self.id = element_id
        self.min_date = min_date
        self.max_date = max_date
        self.initial_visible_month = initial_visible_month or self.min_date

    @property
    def layout(self):
        layout = dbc.Col([html.Div(
                            html.P(self.id,
                                className='text-center m-0 p-0'),
                            style={'color': '#363638'}),
                        dcc.DatePickerSingle(id=self.id,
                                            min_date_allowed=self.min_date,
                                            max_date_allowed=self.max_date,
                                            initial_visible_month=self.initial_visible_month,
                                            persistence=True,
                                            persistence_type='session',
                                            style={'width': '100%'})],
                    style={'width': '100%'})
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


class CardLayout:

    def __init__(self, elements: []):
        self.els = elements

    @property
    def layout(self):
        layout = [dbc.Row(x.layout, className='m-24') for x in self.els]
        return dbc.Col(layout)


    @property
    def callbacks(self):
        callbacks = []
        for x in self.els:
            callbacks.extend(x.callbacks)
        return callbacks

    def _requires_dropdown(self):
        return True