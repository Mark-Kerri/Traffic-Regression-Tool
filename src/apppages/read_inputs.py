"""
Module for data exploration in the Streamlit application.

This module provides functionality for uploading, filtering, and visualizing data
using Streamlit. It allows users to select variables, filter timelines, and preview
data in both table and chart formats.
"""

import streamlit as st
import plotly.express as px  # type: ignore
from apppages.utils.excel import spreadsheet_to_df
from apppages.utils.streamlit_tools import (
    visualise_data,
    visualise_data_indexed,
    create_and_show_df,
    stringify,
    growth_df,
)


def main():
    """
    Run the main Streamlit application for data exploration.

    This function sets up the Streamlit interface, handles user inputs,
    and manages the flow of data processing and visualization.
    """
    st.set_page_config(layout="wide")
    st.title("Data Exploration")
    st.sidebar.success(
        "In this page, the user uploads the data for review before any calculation is performed"
    )
    st.header("Upload a Completed Template:")

    input_file_path = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    if st.button("Read spreadsheet", type="primary", use_container_width=True):
        (
            st.session_state.df,
            st.session_state.df_index,
            st.session_state.var_dict,
        ) = spreadsheet_to_df(input_file_path)
        st.session_state.inputs_file_path = input_file_path

    if st.session_state.df is not None:
        st.session_state.timestep = st.selectbox(
            "Confirm data timestep type:",
            options=st.session_state.prd_dict,
            key="timestep_type",
        )

        if st.session_state.timestep:
            if st.button("Confirm", use_container_width=True):
                st.session_state.prd = st.session_state.prd_dict[
                    st.session_state.timestep
                ]

    if st.session_state.prd is not None:
        st.header("Filter Data Visualisations:")

        x_cols = [x for x in st.session_state.df.columns if x[0] == "x"]
        y_cols = [y for y in st.session_state.df.columns if y[0] == "y"]

        if not st.session_state.y_sel_d or not st.session_state.x_sel_d:
            st.session_state.y_sel_d = y_cols
            st.session_state.x_sel_d = x_cols

        st.session_state.y_sel = st.multiselect(
            "Choose the dependent variables (blank defaults to all):", options=y_cols
        )
        st.session_state.x_sel = st.multiselect(
            "Choose independent variables (blank defaults to all):",
            options=x_cols,
        )

        slider_range = st.select_slider(
            "Choose the range of points to be plotted",
            options=range(0, len(st.session_state.df)),
            value=(0, len(st.session_state.df) - 1),
            format_func=stringify,
        )
        st.session_state.slider_value_start, st.session_state.slider_value_end = (
            slider_range
        )

        col1, col2 = st.columns([1, 1])
        data_container = st.container()

        with col1:
            if st.button("Preview selected data", use_container_width=True):
                # Use x_cols if x_sel is empty, otherwise use x_sel
                x_vars = (
                    x_cols if not st.session_state.x_sel else st.session_state.x_sel
                )
                # Use y_cols if y_sel is empty, otherwise use y_sel
                y_vars = (
                    y_cols if not st.session_state.y_sel else st.session_state.y_sel
                )

                st.session_state.y_sel_d = y_vars
                st.session_state.x_sel_d = x_vars
                st.rerun()

        with col2:
            if st.button("Preview all data", use_container_width=True):
                st.session_state.y_sel_d = y_cols
                st.session_state.x_sel_d = x_cols
                st.rerun()

        data_selection_buttons(
            st.session_state.slider_value_start,
            st.session_state.slider_value_end,
            st.session_state.x_sel_d,
            st.session_state.y_sel_d,
            data_container,
        )

    st.divider()

    if st.button("Clear cache", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]

    if st.button("Next Page", use_container_width=True):
        st.switch_page("apppages/regression_ranking_refactored.py")


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

        st.subheader("Raw data chart")
        visualise_data(filt_df)

        st.subheader("Indexed data chart")
        visualise_data_indexed(filt_df)

        st.subheader("Year on year chart (dummy variables excluded)")
        st.session_state.g_df, st.session_state.g_df_idx = growth_df(filt_df)
        visualise_data(st.session_state.g_df, as_percent=True)

        st.subheader("Correlation Heatmap (Numerical Variables)")
        st.markdown(
            "Use this heatmap to check for strong correlations between your numerical variables. "
            "Values close to 1.0 (dark red) or -1.0 (dark blue) indicate a strong relationship."
        )

        # Get a list of the variable names from the filtered dataframe's columns
        all_vars = filt_df.columns.tolist()

        # Filter this list to only include variables defined as 'value' (i.e., numerical)
        # We slice the column name (e.g., 'y:Sales'[2:]) to look it up in the var_dict
        value_vars = [
            var for var in all_vars if st.session_state.var_dict.get(var[2:]) == "value"
        ]

        # Only attempt to create a correlation matrix if there are at least 2 numerical variables
        if len(value_vars) > 1:
            corr_matrix = filt_df[value_vars].corr().round(3)

            # Create the heatmap using Plotly Express
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,  # Automatically display the correlation values on the heatmap
                aspect="auto",
                color_continuous_scale="RdBu",  # A good color scale for correlations (-1 to 1)
                title="Correlation Matrix",
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info(
                "At least two numerical (value-type) variables must be "
                "selected to display a correlation heatmap."
            )

        st.subheader(
            "Dependent Variable (Y) vs. Independent Variables (X) Relationships"
        )
        st.markdown(
            "Select a dependent variable, then click on the tabs to see its relationship "
            "with each independent variable."
        )

        # y_vars = [c for c in filt_df.columns if c.startswith('y:')]
        # x_vars = [c for c in filt_df.columns if c.startswith('x:')]

        if y_sel and x_sel:
            selected_y_var = st.selectbox(
                "Select a Dependent Variable:",
                options=y_sel,
                key="y_var_selector_for_tabs",  # Add a unique key
            )

            if selected_y_var:
                # Create a clean list of X variable names for the tab titles
                # e.g., "x: GDP" becomes "GDP"
                clean_x_names = [x[2:] for x in x_sel]

                # Create a tab for each independent variable
                tabs = st.tabs(clean_x_names)

                # Loop through each tab and its corresponding x_variable
                for tab, x_var in zip(tabs, x_sel):
                    with tab:
                        # Create a simple scatter plot for the current tab
                        fig_scatter = px.scatter(
                            filt_df,
                            x=x_var,
                            y=selected_y_var,
                            title=f"Relationship between {selected_y_var[2:]} and {x_var[2:]}",
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning(
                "Both dependent (Y) and independent (X) variables "
                "must be selected to display these charts."
            )


if __name__ == "__page__":
    main()
