import plotly.graph_objects as go
from package.layout.base.data_card import DataCard
from pprint import pprint
import pandas as pd


class AreaDataCard(DataCard):
    def __init__(self, data=None, **kwargs):
        super(AreaDataCard, self).__init__(data=data, **kwargs)
        # default capitalizing important
        self.fig_object = kwargs.get("fig_object", "Treemap")

    def _get_figure(self, data):
        fig = go.Figure()
        # We can add types here
        fig_type = getattr(go, self.fig_object)

        figure_colors = self.colors.get("fig")

        for name, df in data.items():

            treemap_df = self.build_hierarchical_dataframe(
                df.reset_index(),
                levels=df.index.names,
                value_column=df.columns[0],
                total_id=name,
            )

            scale_max = round(
                df[df.columns[0]].max() / df[df.columns[0]].sum() * 100, 2
            )

            fig.add_trace(
                fig_type(
                    parents=treemap_df["parent"],
                    labels=treemap_df["id"],
                    values=treemap_df["value"],
                    branchvalues="total",
                    marker=dict(
                        colors=treemap_df["color"],
                        colorscale=figure_colors.get(
                            name, next(iter(figure_colors.values()))
                        ),
                        cmin=0,
                        cmid=scale_max / 3,
                        cmax=scale_max,
                    ),
                    # hovertemplate='<b>%{label} </b> <br> ' +
                    # str(df.columns[0]) +
                    # ' : %{value}<br> Percentage of total: %{color:.2f}',
                    textinfo="label+value+percent parent",
                )
            )

        return fig

    #################
    #    HELPERS    #
    #################

    def build_hierarchical_dataframe(self, df, levels, value_column, total_id="total"):
        """
        Build a hierarchy of levels for Sunburst or Treemap charts.

        Levels are given starting from the bottom to the top of the hierarchy,
        ie the last level corresponds to the root.

        Taken from plotly documentation.
        """
        levels = levels[::-1]
        df_all_trees = pd.DataFrame(columns=["id", "parent", "value", "color"])
        for i, level in enumerate(levels):
            df_tree = pd.DataFrame(columns=["id", "parent", "value", "color"])
            dfg = df.groupby(levels[i:]).sum()
            dfg = dfg[dfg[dfg.columns[0]] > 0]
            dfg = dfg.reset_index()
            df_tree["id"] = dfg[level].copy()
            if i < len(levels) - 1:
                df_tree["parent"] = dfg[levels[i + 1]].copy()
            else:
                df_tree["parent"] = total_id
            df_tree["value"] = dfg[value_column]
            df_tree["color"] = dfg[value_column]
            df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
        total = pd.Series(
            dict(
                id=total_id,
                parent="",
                value=df[value_column].sum(),
                color=df[value_column].sum(),
            )
        )
        df_all_trees = df_all_trees.append(total, ignore_index=True)
        try:
            df_all_trees["color"] = (
                df_all_trees["color"] / df_all_trees["color"].max() * 100
            )
        except ZeroDivisionError as e:
            print(e)
        return df_all_trees
