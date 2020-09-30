import plotly.graph_objects as go
import pandas as pd

from package.layout.base.data_card import DataCard


class ChartDataCard(DataCard):
    def __init__(self, data: {str: pd.DataFrame} = None, **kwargs):

        super(ChartDataCard, self).__init__(data=data, **kwargs)

        # Capitalizing is important here, because we are going to get the same object name from plotly
        self.fig_object = kwargs.get("fig_object", "Scatter")
        self.bar_mode = kwargs.get("bar_mode", "stack")

    def _get_figure(self, data: {str: pd.DataFrame} = None):
        fig = go.Figure()

        FigType = getattr(go, self.fig_object)

        for name, df in data.items():
            fig.add_trace(
                FigType(
                    x=df.index,
                    y=df[df.columns[0]],
                    name=name,
                    marker_color=self.colors.get("fig").get(name),
                    hoverinfo="x+y",
                )
            )
            if self.bar_mode == "overlay":
                fig.update_traces(
                    marker_color="rgb(211, 41, 61)",
                    textposition="inside",
                    texttemplate="%{x:%}",
                    orientation="h",
                    y=df.index,
                    x=df[df.columns[0]],
                    showlegend=False,
                    hoverinfo="none",
                )

        self.style_figure(fig)

        if self.fig_object == "Bar":
            fig.update_layout(barmode=self.bar_mode)

        return fig

    def style_figure(self, fig):
        if self.fig_object == "Scatter":
            self.style_as_scatter(fig)

        fig.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            margin=dict(pad=20),
        )

        fig.update_layout(
            {
                "plot_bgcolor": "rgba(255, 255, 255, 1)",
                "paper_bgcolor": "rgba(255, 255, 255, 1)",
            },
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=True, zeroline=False, gridcolor="LightGray"),
        )

    def style_as_scatter(self, fig):
        fig.update_traces(marker=dict(symbol="square", size=10))
        fig.update_traces(line=dict(width=2))
