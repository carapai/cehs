import statistics
import geojson

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from package.layout.base.data_card import DataCard

import json


class MapDataCard(DataCard):
    def __init__(self, geodata, locations, data: {str: pd.DataFrame} = None, **kwargs):
        super(MapDataCard, self).__init__(data=data, **kwargs)

        # private members
        self.__geojson = None

        # required public members
        self.__set_geo_data(geodata, tolerance=kwargs.get("map_tolerance"))
        self.locations = locations  # TODO: make detection of the geo index automatic

        # optional public members
        self.mapbox_style = "carto-positron"
        self.zoom = 5.50
        self.opacity = 1

    # Content

    def _get_figure(self, data: {str: pd.DataFrame} = None) -> go.Figure:
        """Create and get a figure based on dataframe using Chloroplethmapbox library

        Args:
            data (pandas.DataFrame, optional): data column to render as figure. Defaults to None.

        Returns:
            plotly.graph_objects.Figure: figure to display in datacard layout
        """

        choropleth_map = go.Choroplethmapbox()

        figure_colors = self.colors.get("fig")

        for name, df in data.items():
            choropleth_map = go.Choroplethmapbox(
                z=df[df.columns[0]],
                geojson=self.__geojson,
                locations=df.reset_index()[self.locations],
                hovertemplate="%{location} <br>"
                + df.columns[0]
                + ": %{z}"
                + "<extra></extra>",
                marker_opacity=self.opacity,
                marker_line_width=1,
                colorscale=figure_colors.get(name, next(iter(figure_colors.values()))),
                zauto=True,
                zmid=0,
            )

        fig = go.Figure(choropleth_map)

        # Update the map
        fig.update_layout(
            mapbox_style=self.mapbox_style,
            mapbox_zoom=self.zoom,
            mapbox_center=self.bounds.get("center"),
        )

        # Update of the layout is done in the data card
        return fig

    def __get_geojson_from_data(self, data, id="id"):
        assert id in data.columns, f"GeoDataFrame should contain {id} column"
        geojson_df = json.loads(data.set_index(id).to_json())

        return geojson_df

    def __set_geo_data(self, gdf, tolerance=None, id="id"):
        """Defines the json data for mapping from a geopandas dataframe.

        Args:
            gdf([type]): [description]
            tolerance(float, optional): Allows for faster loading time of map during callback by "rounding" the borders(higher values=faster loading=less precision on border outline). Defaults to None.
            geometry(str, optional): [description]. Defaults to 'geometry'.
            id(str, optional): [description]. Defaults to 'id'.
        """
        if tolerance:
            gdf["geometry"] = gdf["geometry"].simplify(tolerance=tolerance)
        # Set bounds
        bounds = gdf.bounds
        bounds = {
            "xmin": bounds.minx.min(),
            "xmax": bounds.maxx.max(),
            "ymin": bounds.miny.min(),
            "ymax": bounds.maxy.max(),
        }
        bounds["center"] = {
            "lon": np.mean([bounds.get("xmin"), bounds.get("xmax")]),
            "lat": np.mean([bounds.get("ymin"), bounds.get("ymax")]),
        }

        self.bounds = bounds

        self.__geojson = self.__get_geojson_from_data(gdf, id=id)
