import dash_html_components as html
from flask import send_from_directory
from package import here
from dash_bootstrap_components.themes import BOOTSTRAP
from jupyter_dash import JupyterDash
import dash
from dash import Dash
from dash.dependencies import Output, Input
from pprint import pprint
from package.layout.base.data_card import DataCard


class Dashboard:
    """This is abstract dashboard method
    Every nested class should implement following abstract methods:
        - _set_layout: to set dash.app.layout property
    # TODO: expand the class with default layout
    # TODO: expand the class with default styling
    """

    def __init__(self, mode="default", **kwargs):
        external_stylesheets = [BOOTSTRAP]
        if mode == "jupyter":
            self.app = JupyterDash(external_stylesheets=external_stylesheets)
        else:
            self.app = Dash(external_stylesheets=external_stylesheets)

        app = self.app  # For referencing with the decorator (see line below)
        app.title = "CEHS Uganda"

        @app.server.route("/static/<asset_type>/<path>")
        def static_file(asset_type, path):
            return send_from_directory(here / "static" / asset_type, path)

    ################
    #    LAYOUT    #
    ################

    def _set_layout(self):
        """Method is left deliberately empty. Every child class should implement this class"""
        raise NotImplementedError(
            "Every child class should implement __set_layout method!"
        )

    ###################
    #    EXECUTION    #
    ###################

    def run(self, dev=False, **kwargs):
        self._set_layout()
        self._define_callbacks()
        self.app.run_server(debug=dev, use_reloader=dev, **kwargs)

    def switch_data_set(self, data):
        for x in self.data_cards:
            try:
                if isinstance(x, DataCard) or getattr(x, "data") is not None:
                    x.data = data
                    # x.figure = x._get_figure(x.data)
            except AttributeError as e:
                print(e)

    ###################
    #    CALLBACKS    #
    ###################

    def _define_callbacks(self):
        # TODO: self.data_cards is property of datastory... Move this to datastory or data_cards to dashboard?
        # Datacard level
        for x in self.data_cards:
            if x._requires_dropdown():
                for callback in x.callbacks:
                    self.register_callback(
                        callback.get("input"),
                        callback.get("output"),
                        callback.get("func"),
                    )
        for x in self.ind_elements:  # FIXME
            if x._requires_dropdown():
                for callback in x.callbacks:
                    self.register_callback(
                        callback.get("input"),
                        callback.get("output"),
                        callback.get("func"),
                    )

    def register_callback(self, input_element_params, output_elements_params, function):
        out_set, in_set = self.__define_callback_set(
            output_elements_params, input_element_params
        )

        callback_function = self.__process_callback_function(function)

        self.app.callback(inputs=in_set, output=out_set)(callback_function)

    def __process_callback_function(self, function):
        def callback_wrapper(*input_values):
            value = function(*input_values)
            return value

        return callback_wrapper

    def __define_callback_set(
        self, output_elements_id_prop: [(str, str)], input_element_id_prop: [(str, str)]
    ):

        callback_set_outputs = [
            Output(component_id=component_id, component_property=component_prop)
            for component_id, component_prop in output_elements_id_prop
        ]

        callback_set_input = [
            Input(component_id=component_id, component_property=component_prop)
            for component_id, component_prop in input_element_id_prop
        ]

        return (callback_set_outputs, callback_set_input)
