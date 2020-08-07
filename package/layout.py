import dash_bootstrap_components as dbc
import dash_html_components as html


class Layout:

    """Class that brings layout structure.
    """


    def __init__(self):

        self.__layout = None
        self.__columns = []
        self.__rows = []
        pass


    @property
    def layout(self):
        return self.__layout


    @staticmethod
    def make_dropdown(dropdown_structure, id=None):
        dropdown_layout_component = dbc.Col()

        dropdown_layout_component.



        return dropdown_layout_component