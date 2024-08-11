"""
Module for control of the regression parameters in the Streamlit application.

This module provides a Streamlit-based interface for setting up and running linear regressions.
It allows users to define dependent and independent variables, choose a time range, and view
regression results.
"""

import streamlit as st
import statsmodels.api as sm
from subpages.utils.streamlit_tools import growth_df, stringify_g_df, create_and_show_df


def main():
    """
    Run main function for the 'Regression Control' Streamlit app page.

    It enables users to select regression parameters, update the dataframe, and perform
    linear regression analysis on time series data.

    The function interacts with the Streamlit interface to:
    1. Set the dependent and independent variables.
    2. Define the time range for the analysis.
    3. Optionally add a constant to the regression model.
    4. Display regression results including model parameters and summary statistics.

    Returns:
    None
    """
    st.title("Regression Control")
    st.sidebar.success(
        "In this page, the user sets the dependent variable and timeline "
        "for the linear regressions"
    )
    st.header("Define Regression Parameters:")

    prd = None
    # Load or create growth dataframe if not already available
    if st.session_state.g_df is None and prd is None:
        st.session_state.g_df, st.session_state.g_df_idx = growth_df(
            st.session_state.df
        )

    # Extract independent (x) and dependent (y) variables from the growth dataframe
    x_cols = [x for x in st.session_state.g_df.columns if x[3] == "x"]
    y_cols = [y for y in st.session_state.g_df.columns if y[3] == "y"]

    # User selects the dependent (y) variable
    st.session_state.y_sel_g = st.selectbox(
        "Choose the dependent (endogenous) variable:", options=y_cols
    )

    # User selects the independent (x) variables
    st.session_state.x_sel_g = st.multiselect(
        "Choose independent (exogenous) variables:",
        options=x_cols,
    )

    # Option to add a constant to the regression model
    constant_sel = st.selectbox("Add constant?:", options=["Yes", "No"])

    # Slider for selecting the time range to analyze
    st.session_state.slider_value_start, st.session_state.slider_value_end = (
        st.select_slider(
            "Choose the range of points to be plotted",
            options=range(0, len(st.session_state.g_df)),
            value=(0, len(st.session_state.g_df) - 1),
            format_func=stringify_g_df,
        )
    )

    # Button to update the dataframe based on the selected time range and variables
    if st.button("Update dataframe"):
        st.session_state.r_df = create_and_show_df(
            st.session_state.g_df,
            st.session_state.slider_value_start,
            st.session_state.slider_value_end,
            st.session_state.x_sel_g,
            st.session_state.y_sel_g,
        )

    # Try to fit a linear regression model and display the results
    try:
        if (
            st.session_state.x_sel_g is not None
            and st.session_state.y_sel_g is not None
        ):
            if st.session_state.r_df is not None:
                y = st.session_state.r_df[st.session_state.y_sel_g][
                    st.session_state.slider_value_start : st.session_state.slider_value_end
                ]
                if constant_sel == "Yes":
                    x = st.session_state.r_df[st.session_state.x_sel_g][
                        st.session_state.slider_value_start : st.session_state.slider_value_end
                    ]
                    x = sm.add_constant(x, prepend=False)
                else:
                    x = st.session_state.r_df[st.session_state.x_sel_g][
                        st.session_state.slider_value_start : st.session_state.slider_value_end
                    ]

                model = sm.OLS(y, x).fit()
                st.text(model.summary())
                st.session_state.model_params = dict(model.params)
    except ValueError:
        st.error("Please make sure you chose at least one independent (x) variable.")
    except KeyError:
        st.error("Please click the Update Dataframe button to reload the data.")


if __name__ == "__page__":
    main()
