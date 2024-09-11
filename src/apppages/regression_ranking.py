"""
Module for control of the regression parameters in the Streamlit application.

This module provides a Streamlit-based interface for setting up and running linear regressions.
It allows users to define dependent and independent variables, choose a time range, and view
regression results.
"""

import itertools
import pandas as pd
import streamlit as st
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import OLSInfluence
import plotly.express as px
from apppages.utils.streamlit_tools import stringify, growth_df, stringify_g_df, create_and_show_df
import os
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
    st.title("Regression Ranking Creation")
    st.sidebar.success(
        "In this page, the user sets the dependent variable and timeline "
        "for the linear regressions to run in all possible combinations of independent variables "
        "and then being ranked and sorted based on pre-determined metrics"
    )
    if st.session_state.df is not None:
        # Load or create growth dataframe if not already available
        if st.session_state.g_df is None:
            st.session_state.g_df, st.session_state.g_df_idx = growth_df(
                st.session_state.df
            )

        # Extract independent (x) and dependent (y) variables from the growth dataframe
        st.header("Define Regression Parameters:")

        x_cols = [x for x in st.session_state.g_df.columns if x[3] == "x"]
        y_cols = [y for y in st.session_state.g_df.columns if y[3] == "y"]

        # User selects the dependent (y) variable
        st.session_state.y_sel_g = st.selectbox(
            "Choose the dependent (endogenous) variable:", options=y_cols
        )
        st.session_state.x_sel_g = x_cols

        # Option to add a constant to the regression model
        # st.session_state.constant_sel = st.selectbox("Add constant?:", options=["Yes", "No"])
        st.session_state.constant_sel = st.checkbox("Include constant", value=True)
        st.session_state.growth_df_checkbox = st.checkbox("Display growth rates table", value=False)

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
        if st.button("Run all regressions"):
            st.session_state.r_df = create_and_show_df(
                st.session_state.g_df,
                st.session_state.slider_value_start,
                st.session_state.slider_value_end,
                st.session_state.x_sel_g,
                st.session_state.y_sel_g,
                display_df=st.session_state.growth_df_checkbox,
            )
            # start a new outputs df and reset(?) all relevant session_state variables
            st.session_state.model_regressions_list = []
            st.session_state.model_r_squared = []
            st.session_state.regression_rank_dict = {}
            st.session_state.regr_tests_and_cols_dict = {}
            st.session_state.model_regressions_df = pd.DataFrame(
                columns=st.session_state.x_sel_g
            )
            st.session_state.model_regressions_df["const"] = None
            # st.text(x_cols)

            # Try to fit a linear regression model and display the results
            st.session_state.n_counter = 0
            for x_elements in range(len(x_cols)):
                x_combinations = list(itertools.combinations(x_cols, x_elements))
                for x_combo in x_combinations:
                    st.session_state.x_sel_reg = [
                        x for x in st.session_state.x_sel_g if x in list(x_combo)
                    ]
                    try:
                        if (
                            st.session_state.x_sel_g is not None
                            and st.session_state.y_sel_g is not None
                        ):
                            if st.session_state.r_df is not None:
                                y = st.session_state.r_df[st.session_state.y_sel_g][
                                    st.session_state.slider_value_start : st.session_state.slider_value_end
                                ]
                                if st.session_state.constant_sel == True:
                                    x = st.session_state.r_df[
                                        st.session_state.x_sel_reg
                                    ][
                                        st.session_state.slider_value_start : st.session_state.slider_value_end
                                    ]
                                    x = sm.add_constant(
                                        x, prepend=False, has_constant="add"
                                    )
                                else:
                                    x = st.session_state.r_df[
                                        st.session_state.x_sel_reg
                                    ][
                                        st.session_state.slider_value_start : st.session_state.slider_value_end
                                    ]

                                model = sm.OLS(y, x).fit()

                                # compute the residuals and other metrics
                                st.session_state.reg_influence = model
                                # st.write(influence.results)
                                st.session_state.model_params = dict(model.params)
                                test_name_list = [
                                    item.split("x:")[1]
                                    for item in st.session_state.x_sel_reg
                                    if "x:" in item
                                ]
                                test_name = "-".join(test_name_list)
                                st.session_state.model_regressions_list.append(
                                    test_name
                                )
                                st.session_state.model_r_squared.append(
                                    model.rsquared_adj
                                )

                                # Select only the keys that are in the columns
                                filtered_dicts = [
                                    {
                                        key: value
                                        for key, value in st.session_state.model_params.items()
                                        if key
                                        in st.session_state.model_regressions_df.columns
                                    }
                                ]

                                # Append the row
                                st.session_state.model_regressions_df = pd.concat(
                                    [
                                        st.session_state.model_regressions_df,
                                        pd.DataFrame(
                                            filtered_dicts,
                                            columns=st.session_state.model_regressions_df.columns,
                                        ),
                                    ]
                                )
                                st.session_state.regression_rank_dict[test_name] = (
                                    model.summary()
                                )
                                st.session_state.regr_tests_and_cols_dict[test_name] = (
                                    st.session_state.x_sel_reg
                                )
                                st.session_state.reg_residuals[test_name] = model.resid
                                st.session_state.reg_fitted_vals[test_name] = model.fittedvalues
                                st.session_state.n_counter += 1
                    except ValueError:
                        st.error(
                            "Please make sure you chose at least one independent (x) variable."
                        )
                    except KeyError:
                        st.error(
                            "Please click the Update Dataframe button to reload the data."
                        )
            st.session_state.model_regressions_df["r_squared"] = (
                st.session_state.model_r_squared
            )
            st.session_state.model_regressions_df["Test name"] = (
                st.session_state.model_regressions_list
            )
            columns = ["r_squared"] + [
                col
                for col in st.session_state.model_regressions_df.columns
                if col != "r_squared"
            ]
            st.session_state.model_regressions_df = (
                st.session_state.model_regressions_df[columns]
            )
            st.session_state.model_regressions_df = (
                st.session_state.model_regressions_df.set_index("Test name")
            )
            st.session_state.model_regressions_df = (
                st.session_state.model_regressions_df.sort_values(
                    "r_squared", ascending=False
                )
            )
        if st.session_state.model_regressions_df is not None:
            st.subheader(
                f"Regression outputs for {st.session_state.y_sel_g} "
                f"\n All combinations of independent (x) variables ({st.session_state.n_counter+1} tests), "
                f"\n sorted by adjusted r squared highest to lowest"
            )
            with st.expander("Regression outputs"):
                st.session_state.selected_regression = st.dataframe(
                    st.session_state.model_regressions_df, on_select="rerun"
                )
            try:
                st.session_state.reg_sel = st.text_input(
                    "Select a test from the table above:",
                    value=st.session_state.model_regressions_df.iloc[
                        st.session_state.selected_regression.selection.rows
                    ].index[0],
                )
            except IndexError:
                st.write(":red[**Please select a test from the table above!**]")
        if st.session_state.reg_sel:
            with st.expander("Regression summary table"):
                st.text(st.session_state.regression_rank_dict[st.session_state.reg_sel])
            with st.expander("Regression further outputs"):
                st.text('Regression residuals and fitted values')

                st.session_state.residuals_df = pd.DataFrame()#,index=st.session_state.r_df.index)
                st.session_state.residuals_df['Residuals'] = st.session_state.reg_residuals[st.session_state.reg_sel]
                st.session_state.residuals_df['Fitted values'] = st.session_state.reg_fitted_vals[st.session_state.reg_sel]
                st.session_state.residuals_df['Actuals'] = st.session_state.residuals_df['Residuals']  + st.session_state.residuals_df['Fitted values']

                if st.button('Display residuals data'):
                    st.dataframe(st.session_state.residuals_df)
                # Plot residuals
                # fig = px.line(
                #     st.session_state.residuals_df,
                #     x=st.session_state.residuals_df.index,
                #     y=st.session_state.residuals_df.columns,
                #     title=f"Residuals over time",
                # )
                # fig.update_layout(xaxis_title="Year", yaxis_title="Variable")
                columns = st.multiselect("Columns:", st.session_state.residuals_df.columns)
                st.scatter_chart(data=st.session_state.residuals_df[columns])
                # st.plotly_chart(fig)

                # fig_inf = sm.graphics.influence_plot(st.session_state.reg_influence, criterion="cooks")
                # fig_inf.tight_layout(pad=1.0)
                # st.plotly_chart(fig_inf)

        # base year
        # print(st.session_state.df.head())
        # print(st.session_state.y_sel)
        # print(
        #     st.session_state.df[st.session_state.y_sel][base_year_start: base_year_end + 1]
        # )

        # use the test name entered above to find the parameters from the equivalent test
        if st.session_state.model_regressions_df is not None:
            try:
                coeff_df = pd.DataFrame(
                    st.session_state.model_regressions_df.loc[st.session_state.reg_sel]
                ).transpose()
                st.subheader("Regression coefficients for selected test")
                coeff_df = st.data_editor(coeff_df, num_rows="dynamic")
                # print(coeff_df)
            except KeyError:
                st.write("")

        # pasted backcast code below to be adapted in this page
        st.session_state.y_sel = st.session_state.y_sel_g.split("g: ")[1]

        if st.session_state.selected_regression is not None:
            st.session_state.base_slider_value_start, st.session_state.base_slider_value_end = (
                st.select_slider(
                    "Select the range of points to be used as base year",
                    options=range(0, len(st.session_state.df)),
                    value=(0, len(st.session_state.df) - 1),
                    # on_change=visualise_data,
                    args=(
                        st.session_state.df,
                        st.session_state.base_slider_value_start,
                        st.session_state.base_slider_value_end,
                    ),
                    format_func=stringify,
                )
            )
            base_year_start = st.session_state.base_slider_value_start
            base_year_end = st.session_state.base_slider_value_end
        # print(st.session_state.g_df.columns)
        if (
            st.session_state.base_slider_value_start != 0
            or st.session_state.base_slider_value_end != -1
        ):
            if st.button("Display base year data"):
                st.header("Base year data:")
                st.dataframe(
                    st.session_state.df[st.session_state.y_sel][
                        base_year_start : base_year_end + 1
                    ]
                )
            if st.button("Display growth rates table"):

                st.header("Growth rates")
                # growth rate of GDP
                st.dataframe(st.session_state.g_df[st.session_state.slider_value_start:st.session_state.slider_value_end+1])
        # simplify the variable equal to the growth df columns of the regression test to be analysed
        if (
            st.session_state.reg_sel is not None
            and st.session_state.regr_tests_and_cols_dict != {}
        ):
            reg_cols = st.session_state.regr_tests_and_cols_dict[
                st.session_state.reg_sel
            ]

            elast_df = (
                st.session_state.g_df[reg_cols] ** coeff_df[reg_cols].iloc[0][reg_cols]
            )

            st.header("Backcast:")
            st.session_state.bc_df = pd.DataFrame(
                data=elast_df.shift(periods=-st.session_state.prd),
                index=st.session_state.df.index,
            )

            # copies the e.g 2012/13 growth rate to 2012 row in bc_df
            st.session_state.bc_df[: st.session_state.prd] = elast_df[
                : st.session_state.prd
            ]
            # initialise Combined Growth column
            st.session_state.bc_df["Combined Growth"] = 1  # None
            for col in reg_cols:
                st.session_state.bc_df.loc[
                    st.session_state.bc_df.index[-st.session_state.prd :], col
                ] = 1
            st.session_state.bc_df = st.session_state.bc_df.reset_index()

            st.session_state.bc_df["Predicted y"] = None
            st.session_state.bc_df["Forecasted y"] = None

            # base year value
            base_year = st.session_state.df[st.session_state.y_sel][
                base_year_start : base_year_end + 1
            ]
            base_year_idx = base_year.index.to_list()
            base_year_idx_number = st.session_state.bc_df["index"][
                st.session_state.bc_df["index"] == base_year_idx[-1]
            ].index[0]

            # Copy base year value(s) from user slider selection to the predicted_y
            for base_year_val in base_year_idx:
                st.session_state.bc_df.loc[
                    st.session_state.bc_df["index"] == base_year_val, "Predicted y"
                ] = st.session_state.df.loc[base_year_val, st.session_state.y_sel]

            # loop through the rows starting from the first one to be predicted going up one timestep at a time
            for i in range(
                len(st.session_state.bc_df) - st.session_state.prd - 1,
                -1,
                -st.session_state.prd,
            ):
                # loop through growth (X) columns and calculate Combined Growth (combination of X columns together)
                # backwards in time
                for col in reg_cols:
                    for n in range(st.session_state.prd):
                        st.session_state.bc_df.loc[i - n, "Combined Growth"] = (
                            st.session_state.bc_df.loc[i - n, "Combined Growth"]
                            * st.session_state.bc_df.loc[i - n, col]
                        )
                        # Back-casting is only calculated for any time before base year
                        if st.session_state.bc_df["index"][i] < base_year_idx[0]:
                            st.session_state.bc_df.loc[i - n, "Predicted y"] = (
                                st.session_state.bc_df.loc[
                                    i - n + st.session_state.prd, "Predicted y"
                                ]
                                / st.session_state.bc_df.loc[i - n, "Combined Growth"]
                            )

            # this could have been potentially done in a better way, but it works.
            # Go through rows after base year and forecast growth using values from previous year and growth rate
            for i in range(
                base_year_idx_number + 1,
                len(st.session_state.bc_df),
                st.session_state.prd,
            ):
                for n in range(st.session_state.prd):
                    if i > base_year_idx_number:
                        try:
                            st.session_state.bc_df.loc[i + n, "Forecasted y"] = (
                                st.session_state.bc_df.loc[
                                    i + n - st.session_state.prd, "Predicted y"
                                ]
                                * st.session_state.bc_df.loc[
                                    i + n - st.session_state.prd, "Combined Growth"
                                ]
                            )
                        except TypeError:
                            st.session_state.bc_df.loc[i + n, "Forecasted y"] = (
                                st.session_state.bc_df.loc[
                                    i + n - st.session_state.prd, "Forecasted y"
                                ]
                                * st.session_state.bc_df.loc[
                                    i + n - st.session_state.prd, "Combined Growth"
                                ]
                            )

            # enforce base year values to be equal to the actuals
            for base_year_val in base_year_idx:
                st.session_state.bc_df.loc[
                    st.session_state.bc_df["index"] == base_year_val, "Predicted y"
                ] = st.session_state.df.loc[base_year_val, st.session_state.y_sel]

            # bring back index to be used for x-axis of plots
            st.session_state.bc_df = st.session_state.bc_df.set_index("index")
            # st.session_state.bc_df = st.session_state.bc_df[st.session_state.slider_value_start:st.session_state.slider_value_end+1]
            # convert to float for plotting
            st.session_state.bc_df["Predicted y"] = st.session_state.bc_df[
                "Predicted y"
            ].astype(float)
            st.session_state.bc_df["Forecasted y"] = st.session_state.bc_df[
                "Forecasted y"
            ].astype(float)

            # fill the forecasted y column nans with values from the predicted y column
            st.session_state.bc_df["Forecasted y"] = st.session_state.bc_df[
                "Forecasted y"
            ].fillna(st.session_state.bc_df["Predicted y"])


            st.session_state.bc_df[st.session_state.y_sel] = st.session_state.df[
                st.session_state.y_sel
            ]
            if st.button("Display forecasted y table"):
                st.dataframe(st.session_state.bc_df[st.session_state.slider_value_start:st.session_state.slider_value_end+1+st.session_state.prd])
                # st.text(st.session_state.y_sel)
            # visualise_data(st.session_state.bc_plot_df,0,len(st.session_state.bc_plot_df)-1)
            # to-do: Either modify the visualise_data function to be more flexbile (e.g. add input title)
            #   or create a new visualisation function
            st.session_state.bc_plot_df = st.session_state.bc_df[
                ["Forecasted y", st.session_state.y_sel]
            ]


            st.session_state.bc_plot_df = st.session_state.bc_plot_df[st.session_state.slider_value_start:st.session_state.slider_value_end+1+st.session_state.prd]

            fig = px.line(
                st.session_state.bc_plot_df,
                x=st.session_state.bc_plot_df.index,
                y=st.session_state.bc_plot_df.columns,
                title=f"Forecast on historic data of {st.session_state.y_sel}",
                color_discrete_sequence=st.session_state.custom_colors
            )
            fig.update_layout(xaxis_title="Year", yaxis_title="Variable")
            st.plotly_chart(fig)
            if st.button("Export forecast as html"):
                fig.write_html(os.path.join(st.session_state.output_path,f"Forecast of {st.session_state.y_sel[2:]} "
                                                                     f"({st.session_state.bc_plot_df.index[0]} "
                                                                     f"-{st.session_state.bc_plot_df.index[-1]}).html")
                           ) # Save as HTML

    else:
        st.subheader(
            'Please load traffic data using the "Data exploration" page before navigating back to this page.'
        )


if __name__ == "__page__":
    main()
