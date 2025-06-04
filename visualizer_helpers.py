"""Module containing helper functions for the visualizer module."""

import logging
from pathlib import Path
from typing import Optional, Callable

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


logger = logging.getLogger(__name__)


COLOR_MAP = {
    "Orange_light": "#FAC58F",
    "Marine_light": "#66A8C6",
    "Leaf_light": "#bdddbb",
    "Cherry_light": "#CE5964",
    "Grey_light": "#737380",
    "Orange": "#F68B1F",
    "Marine": "#006FA1",
    "Leaf": "#91C78E",
    "Cherry": "#BA1222",
    "Grey": "#48484A",
}


def create_bar_chart(
    source_data: pd.DataFrame,
    source: str,
    col: str,
    plot_col: str,
    **plot_kwargs,
) -> plotly.graph_objs.Figure:
    """
    Create a bar chart with unweighted and weighted values.

    Args:
        source_data (pd.DataFrame): The dataframe containing the data.
        source (str): The source name to be used as the data name
        col (str): The column name of the variable to plot.
        plot_col (str): The column name of values to plot.
        plot_kwargs: Additional keyword arguments to pass to the plot.

    Returns:
        plotly.graph_objs.Figure: Plotly figure.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=source_data[col],
            y=source_data[plot_col],
            name=source,
            marker_color=list(COLOR_MAP.values())[0],
            **plot_kwargs,
        ),
    )

    return fig


def create_pie_chart(
    df: pd.DataFrame,
    columns: list,
) -> plotly.graph_objs.Figure:
    """
    Create pie charts with unweighted data.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        columns (list): The columns to plot.

    Returns:
        plotly.graph_objs.Figure: Plotly figure.
    """

    # Initialize the subplot grid
    fig = go.Figure()

    # Loop through the columns
    for col, column in enumerate(columns, start=1):
        fig.add_trace(
            go.Pie(
                labels=df.index,
                values=df[column],
                textinfo="label+percent",
                textposition="outside",
                automargin=True,
            ),
        )

    return fig


def get_filters(
    zone_set: str, affected_tazs: list, affected_mazs: list
) -> tuple[Callable, Callable]:
    """
    Define filter functions corresponding to zone_set options

    Each filter will accept a Series with values of TAZ or MAZ ids
    and will return a Series with the same index reresenting whether
    the corresponding value is in the selected zone set.
    """

    # for all zones
    def allow_all(zone_series: pd.Series) -> pd.Series:
        return zone_series.apply(lambda _: True)

    # only zones inside the affected area
    def allow_affected_TAZ(taz_series: pd.Series) -> pd.Series:
        return taz_series.isin(affected_tazs)

    def allow_affected_MAZ(maz_series: pd.Series) -> pd.Series:
        return maz_series.isin(affected_mazs)

    # only zones outside the affected area
    def allow_unaffected_TAZ(taz_series: pd.Series) -> pd.Series:
        return ~allow_affected_TAZ(taz_series)

    def allow_unaffected_MAZ(maz_series: pd.Series) -> pd.Series:
        return ~allow_affected_MAZ(maz_series)

    # select the corresponding filters based on zone_set parameter
    match zone_set:
        case "all":
            return allow_all, allow_all
        case "affected":
            return allow_affected_TAZ, allow_affected_MAZ
        case "unaffected":
            return allow_unaffected_TAZ, allow_unaffected_MAZ
        case _:
            raise f"Unknown zone set: {zone_set}. Acceptable options: 'all','affected','unaffected'"
