"""
Streamlit functionality.

This module provides utility functions for data manipulation and visualization
within the Streamlit application, focusing on time series data.
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


def stringify(i: int = 0) -> str:
    """
    Convert a slider integer index to a corresponding dataframe index string.

    Parameters:
    i (int): The index value from the slider, default is 0.

    Returns:
    str: The corresponding index string from the dataframe.
    """
    return st.session_state.df_index[i]


def create_and_show_df(df, slider_value_start, slider_value_end, x_sel, y_sel):
    """
    Filter and display a dataframe based on selected columns and slider values.

    Parameters:
    df (pd.DataFrame): The dataframe to be filtered.
    slider_value_start (int): The start index for filtering.
    slider_value_end (int): The end index for filtering.
    x_sel (list): List of strings representing the independent variables.
    y_sel (str or list): A string or list of strings representing the dependent variables.

    Returns:
    pd.DataFrame: The filtered dataframe.
    """
    filt_cols = []

    # Check if y_sel is a string or a list and append accordingly
    if isinstance(y_sel, str):
        filt_cols.append(y_sel)
    elif isinstance(y_sel, list):
        for y in y_sel:
            filt_cols.append(y)

    for x in x_sel:
        filt_cols.append(x)

    filt_df = df[slider_value_start : slider_value_end + 1][filt_cols]
    st.dataframe(data=filt_df)

    return filt_df


def visualise_data(df):
    """
    Visualize data with interactive line charts using Plotly and Streamlit.

    Parameters:
    df (pd.DataFrame): The dataframe containing the data to visualize.

    Returns:
    None
    """
    df_idx = df.index
    df_x = pd.DataFrame(index=df_idx)
    df_y = pd.DataFrame(index=df_idx)

    # Split x and y columns into separate dataframes
    for col in df.columns:
        if col[0] == "x":
            df_x[col] = df[col]
        elif col[0] == "y":
            df_y[col] = df[col]

    # Create a line plot for the original data
    fig = px.line(
        df,
        x=df.index,
        y=df.columns,
        title="Interactive chart of each variable over time",
    )
    fig.update_layout(xaxis_title="Timeline", yaxis_title="Variable")
    st.plotly_chart(fig)

    # Create a line plot for the indexed data (base-100)
    df_indexed = 100 * (df / df.iloc[0, :])
    fig = px.line(
        df_indexed,
        x=df_indexed.index,
        y=df_indexed.columns,
        title="Interactive chart of each variable indexed to base-100 over time",
    )
    fig.update_layout(xaxis_title="Timeline", yaxis_title="Indexed variable")
    st.plotly_chart(fig)


def stringify_g_df(i: int = 0) -> str:
    """
    Convert a slider integer index to a corresponding growth dataframe index string.

    Parameters:
    i (int): The index value from the slider, default is 0.

    Returns:
    str: The corresponding index string from the growth dataframe.
    """
    return st.session_state.g_df_idx[i]


def growth_df(df):
    """
    Calculate growth rates for variables in the dataframe based on their types.

    Parameters:
    df (pd.DataFrame): The dataframe containing the original data.

    Returns:
    tuple: A tuple containing the growth dataframe and its index.
    """
    prd = 4  # Quarterly data

    # Identify columns of each type and calculate growth rates
    for df_col in df.columns:
        var_type = st.session_state.var_dict[df_col[2:]]
        if var_type == "abs":
            df["g: " + df_col] = df[df_col].pct_change(periods=prd) + 1
        elif var_type == "pct_val_or_dummy":
            df["g: " + df_col] = np.exp(df[df_col] - df[df_col].shift(prd))
        elif var_type == "pct_change":
            df["g: " + df_col] = df[df_col] + 1

    # Filter growth columns and drop rows with all NaN values
    g_cols = [c for c in df.columns if c.startswith("g:")]
    g_df = df[g_cols].dropna(how="all")
    g_df_idx = g_df.index

    return g_df, g_df_idx


def growth_list(elements):
    """
    Prepend 'g: ' to a list of elements, typically variable names.

    Parameters:
    elements (list): A list of strings representing variable names.

    Returns:
    list: A list of strings with 'g: ' prepended to each variable name.
    """
    return [f"g: {element}" for element in elements]
