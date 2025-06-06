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
            format_func=lambda i: stringify(st.session_state.df, i),
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

        # Add a header to the sidebar for our new controls
        st.sidebar.divider()
        st.sidebar.header("Chart & Table View Options")

        # The radio button to control the view
        view_choice = st.sidebar.radio(
            "Select a data view for the charts and tables:",
            ["All Selected", "Dependent (Y) Only", "Independent (X) Only"],
            index=0,  # Default to "All Selected"
        )

        # Determine which variables to show based on the user's choice
        y_vars_to_show = []
        x_vars_to_show = []

        if view_choice == "All Selected":
            y_vars_to_show = st.session_state.y_sel_d
            x_vars_to_show = st.session_state.x_sel_d
        elif view_choice == "Dependent (Y) Only":
            y_vars_to_show = st.session_state.y_sel_d
            x_vars_to_show = []
        elif view_choice == "Independent (X) Only":
            y_vars_to_show = []
            x_vars_to_show = st.session_state.x_sel_d

        # Call the (new) visualization function with the correctly filtered variable lists
        render_visualizations(
            st.session_state.slider_value_start,
            st.session_state.slider_value_end,
            x_vars_to_show,
            y_vars_to_show,
            data_container,
        )

    st.divider()

    if st.button("Clear cache", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]

    if st.button("Next Page", use_container_width=True):
        st.switch_page("apppages/regression_ranking_refactored.py")


# In read_inputs.py, replace your visualization function with this new version:


def render_visualizations(
    slider_value_start: int,
    slider_value_end: int,
    x_sel: list,
    y_sel: list,
    container,
) -> None:
    """
    Renders filtered data tables and charts within a Streamlit container
    based on a view selected by the user.

    Args:
        slider_value_start (int): The start index for data filtering.
        slider_value_end (int): The end index for data filtering.
        x_sel (list): List of selected independent variables for the current view.
        y_sel (list): List of selected dependent variables for the current view.
        container (st.container): Streamlit container to display the visualizations.
    """
    with container:
        if not y_sel and not x_sel:
            st.warning(
                "Please select at least one dependent or independent variable to view."
            )
            return  # Exit the function if nothing is selected

        # --- Standard Visualizations ---
        st.header("Time Series Visualizations:")

        # Create the filtered dataframe based on the current view
        st.subheader("Data Table")
        filt_df = create_and_show_df(
            st.session_state.df,
            slider_value_start,
            slider_value_end,
            x_sel,
            y_sel,
        )

        st.subheader("Data Chart")
        visualise_data(filt_df)

        st.subheader("Indexed Data Chart (Base 100)")
        visualise_data_indexed(filt_df)

        st.subheader("Year-on-Year Growth (Value-Type Variables)")
        st.session_state.g_df, st.session_state.g_df_idx = growth_df(filt_df)
        visualise_data(st.session_state.g_df, as_percent=True)

        # --- Correlation and Relationship Analysis ---
        st.header("Variable Relationship Analysis")

        # --- Correlation Heatmap (only shown if there are numerical variables) ---
        st.subheader("Correlation Heatmap")
        value_vars = [
            var
            for var in filt_df.columns
            if st.session_state.var_dict.get(var[2:]) == "value"
        ]
        if len(value_vars) > 1:
            corr_matrix = filt_df[value_vars].corr().round(3)
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu",
                title="Correlation Matrix of Numerical Variables",
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info(
                "Select at least two numerical variables to display a correlation heatmap."
            )

        # --- Y vs. X Relationship (only shown when BOTH Y and X are available) ---
        # This uses the original, unfiltered selections to allow comparisons
        original_y_sel = st.session_state.y_sel_d
        original_x_sel = st.session_state.x_sel_d

        if original_y_sel and original_x_sel:
            st.divider()
            st.header("Explore Dependent vs. Independent Relationships")

            # Create the full dataframe needed for this specific chart
            full_filt_df = create_and_show_df(
                st.session_state.df,
                slider_value_start,
                slider_value_end,
                original_x_sel,
                original_y_sel,
                display_df=False,
            )

            selected_y_var = st.selectbox(
                "Select a Dependent Variable:",
                options=original_y_sel,
                key="y_var_selector_for_tabs",
            )

            if selected_y_var:
                clean_x_names = [x[2:] for x in original_x_sel]
                tabs = st.tabs(clean_x_names)

                for tab, x_var in zip(tabs, original_x_sel):
                    with tab:
                        fig_scatter = px.scatter(
                            full_filt_df,
                            x=x_var,
                            y=selected_y_var,
                            title=f"Relationship between {selected_y_var[2:]} and {x_var[2:]}",
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)


if __name__ == "__page__":
    main()
