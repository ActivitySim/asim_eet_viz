"""Module containing helper functions for the visualizer module."""

import logging
from pathlib import Path
from typing import Optional

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
