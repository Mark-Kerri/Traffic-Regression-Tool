"""
Module for data exploration in the Streamlit application.

This module provides functionality for uploading, filtering, and visualizing data
using Streamlit. It allows users to select variables, filter timelines, and preview
data in both table and chart formats.
"""

import streamlit as st
from apppages.utils.excel import spreadsheet_to_df
from apppages.utils.streamlit_tools import visualise_data, create_and_show_df, stringify

DEFAULT_FILE_PATH_FOR_TESTING = r"C:\Fidias\Coding-related\Python\Traffic-Regression-Tool\data\reg_input\Development Annual Traffic Data Regression Inputs.xlsx"


def main():
    """
    Run the main Streamlit application for data exploration.

    This function sets up the Streamlit interface, handles user inputs,
    and manages the flow of data processing and visualization.
    """
    st.title("Data Exploration")
    st.sidebar.success(
        "In this page, the user uploads the data for review before any calculation is performed"
    )
    st.header("Upload a Completed Template:")

    input_file_path = st.text_input(
        "Enter the full file path (without quotes):",
        value=st.session_state.inputs_file_path,
        # value=DEFAULT_FILE_PATH_FOR_TESTING, # use this when testing
    )

    if st.button("Read spreadsheet"):
        (
            st.session_state.df,
            st.session_state.df_index,
            st.session_state.var_dict,
            st.session_state.timestep,
        ) = spreadsheet_to_df(input_file_path)
        print(st.session_state.timestep)
        st.session_state.prd = st.session_state.prd_dict[st.session_state.timestep]
        st.session_state.inputs_file_path = input_file_path

    if st.session_state.df is not None:
        st.header("Filter Timeline:")
        st.session_state.slider_value_start, st.session_state.slider_value_end = (
            st.select_slider(
                "Choose the range of points to be plotted",
                options=range(0, len(st.session_state.df)),
                value=(0, len(st.session_state.df) - 1),
                format_func=stringify,
            )
        )

        x_cols = [x for x in st.session_state.df.columns if x[0] == "x"]
        y_cols = [y for y in st.session_state.df.columns if y[0] == "y"]
        st.header("Filter Data Variables:")
        st.session_state.y_sel = st.multiselect(
            "Choose the dependent (endogenous) variable:", options=y_cols
        )
        st.session_state.x_sel = st.multiselect(
            "Choose independent (exogenous) variables:",
            options=x_cols,
        )

        col1, col2 = st.columns([1, 1])
        data_container = st.container()

        with col1:
            if st.button("Preview selected data"):
                # Use x_cols if x_sel is empty, otherwise use x_sel
                x_vars = (
                    x_cols if not st.session_state.x_sel else st.session_state.x_sel
                )
                # Use y_cols if y_sel is empty, otherwise use y_sel
                y_vars = (
                    y_cols if not st.session_state.y_sel else st.session_state.y_sel
                )

                data_selection_buttons(
                    st.session_state.slider_value_start,
                    st.session_state.slider_value_end,
                    x_vars,
                    y_vars,
                    data_container,
                )
        with col2:
            if st.button("Preview all data"):
                data_selection_buttons(
                    st.session_state.slider_value_start,
                    st.session_state.slider_value_end,
                    x_cols,
                    y_cols,
                    data_container,
                )


def data_selection_buttons(
    slider_value_start: int,
    slider_value_end: int,
    x_sel: list,
    y_sel: list,
    container,
) -> None:
    """
    Display selected data in a table and chart format.

    This function filters the data based on the selected range and variables,
    then displays it in a table and chart format within the specified Streamlit container.

    Args:
        slider_value_start (int): The start index for data filtering.
        slider_value_end (int): The end index for data filtering.
        x_sel (list): List of selected independent variables.
        y_sel (list): List of selected dependent variables.
        container (st.container): Streamlit container to display the data and charts.

    Returns:
        None
    """
    with container:
        st.header("Datatable")
        filt_df = create_and_show_df(
            st.session_state.df,
            slider_value_start,
            slider_value_end,
            x_sel,
            y_sel,
        )

        st.header("Charts")
        visualise_data(filt_df)


if __name__ == "__page__":
    main()
