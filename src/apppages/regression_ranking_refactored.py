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
from apppages.utils.streamlit_tools import stringify, log_df, create_and_show_df, stringify_l_df, backcast_df
import os
import math
import numpy as np

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
        if st.session_state.log_df is None:
            st.session_state.log_df,st.session_state.l_df_idx = log_df(st.session_state.df)

        # Extract independent (x) and dependent (y) variables from the growth dataframe
        st.header("Define Regression Parameters:")
        st.session_state.x_sel_l = [x for x in st.session_state.log_df.columns if x[3] == "x"]
        y_cols = [y for y in st.session_state.log_df.columns if y[3] == "y"]

        # User selects the dependent (y) variable
        st.session_state.y_sel_l = st.selectbox(
            "Choose the dependent variable:", options=y_cols
        )

        # Option to add a constant to the regression model
        st.session_state.constant_sel = st.checkbox("Include constant", value=True)

        # Slider for selecting the time range to analyze
        st.session_state.slider_value_start, st.session_state.slider_value_end = (
            st.select_slider(
                "Choose the range of points to be plotted",
                options=range(0, len(st.session_state.log_df)),
                value=(0, len(st.session_state.log_df) - 1),
                format_func=stringify_l_df,
            )
        )

        with st.expander("Advanced filters"):
            st.subheader('Skip variable combinations')
            st.markdown('Set the pairs to zero in the matrix below so that those pairs are not used as part of a regerssion model at the same time:')
            # st.text(st.session_state.x_sel_l)
            x_interaction_table_full = pd.DataFrame(data = 1,index = st.session_state.x_sel_l, columns = st.session_state.x_sel_l)
            bool_matrix = np.triu(np.ones(x_interaction_table_full.shape)).astype(bool)
            x_interaction_table = x_interaction_table_full.where(bool_matrix)
            st.session_state.x_interaction_table = st.data_editor(x_interaction_table, num_rows="dynamic")

            st.session_state.x_inter_stack = st.session_state.x_interaction_table.stack().reset_index()
            st.session_state.x_inter_stack.columns = ['X_1','X_2','Value']
            st.session_state.x_inter_stack = st.session_state.x_inter_stack[st.session_state.x_inter_stack['Value'] == 0]
            st.session_state.x_combos_to_exclude = list(st.session_state.x_inter_stack[['X_1','X_2']].values)
            if st.session_state.n_counter > 0:
                st.subheader('Parameter filtering')
                st.markdown('')

                st.session_state.parameter_filters = pd.DataFrame(data=st.session_state.regressions_min_max_df.T)#, columns = ['Min','Max'])#,index = st.session_state.x_sel_l + ['r_squared'])
                st.session_state.parameter_filters.columns = ['Min','Max']
                parameter_filters = st.data_editor(st.session_state.parameter_filters, num_rows="dynamic")
                param_t = parameter_filters.T
                # st.data_editor(param_t)
                if st.button('Apply filters'):
                    st.session_state.model_regressions_filtered = st.session_state.model_regressions_df
                    st.session_state.model_regressions_df = st.session_state.model_regressions_df.astype(
                        float)

                    for col in param_t:
                        print(st.session_state.regressions_min_max_df.T)
                        # print(float(param_t.loc['Min',col]))
                        # print(len(st.session_state.model_regressions_df[col]))
                        st.session_state.model_regressions_filtered[col] = st.session_state.model_regressions_df[
                            (st.session_state.model_regressions_df[col] >= float(param_t.loc['Min', col])) &
                            (st.session_state.model_regressions_df[col] <= float(param_t.loc['Max', col]))
                            ][col]

                        if param_t.loc['Min', col] != st.session_state.regressions_min_max_df.T.loc[col, 0] or \
                                param_t.loc['Max', col] != st.session_state.regressions_min_max_df.T.loc[col, 1]:

                            st.session_state.model_regressions_filtered = st.session_state.model_regressions_filtered[
                                st.session_state.model_regressions_filtered[col].notna()
                                # Removes rows where col is None or NaN
                            ]
                        # st.session_state.model_regressions_df[col] = st.session_state.model_regressions_df[col].astype(str)
                        # break
                # print(st.session_state.model_regressions_df.dtypes)
                # st.session_state.model_regressions_df =



        # Button to update the dataframe based on the selected time range and variables
        if st.button("Run all regressions"):
            st.session_state.r_df = create_and_show_df(
                st.session_state.log_df,
                st.session_state.slider_value_start,
                st.session_state.slider_value_end,
                st.session_state.x_sel_l,
                st.session_state.y_sel_l,
                display_df=True,
            )
            # start a new outputs df and reset(?) all relevant session_state variables
            st.session_state.model_regressions_list = []
            st.session_state.model_r_squared = []
            st.session_state.regression_rank_dict = {}
            st.session_state.regr_tests_and_cols_dict = {}
            st.session_state.model_regressions_df = pd.DataFrame(
                columns=st.session_state.x_sel_l
            )
            st.session_state.model_regressions_df["const"] = None
            st.session_state.model_regressions_df["r_squared"] = None
            st.session_state.model_regressions_df["Test name"] = None

            # Try to fit a linear regression model and display the results
            st.session_state.n_counter = 0
            for x_elements in range(len(st.session_state.x_sel_l)):
                x_combinations = list(itertools.combinations(st.session_state.x_sel_l, x_elements))
                for i, x_combo in enumerate(x_combinations):
                    exclude = False
                    for pair in st.session_state.x_combos_to_exclude:
                        if set(pair).issubset(set(x_combo)):
                            exclude = True
                            break
                    if not exclude:
                        st.session_state.x_sel_reg = [
                            x for x in st.session_state.x_sel_l if x in list(x_combo)
                        ]
                        try:
                            if (
                                st.session_state.x_sel_l is not None
                                and st.session_state.y_sel_l is not None
                            ):
                                if st.session_state.r_df is not None:
                                    y = st.session_state.r_df[st.session_state.y_sel_l][
                                        st.session_state.slider_value_start : st.session_state.slider_value_end +1
                                    ]
                                    if st.session_state.constant_sel == True:
                                        x = st.session_state.r_df[
                                            st.session_state.x_sel_reg
                                        ][
                                            st.session_state.slider_value_start : st.session_state.slider_value_end
                                        +1]
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

                                    filtered_dicts[0]["r_squared"] = model.rsquared_adj
                                    filtered_dicts[0]["Test name"] = test_name

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

                                    # if x_elements == len(st.session_state.x_sel_l) - 1 and i == len(x_combinations) - 1:




                                    st.session_state.n_counter += 1
                        except ValueError:
                            st.error(
                                "Please make sure you chose at least one independent (x) variable."
                            )


        if st.session_state.model_regressions_df is not None:
            if "Test name" in st.session_state.model_regressions_df.columns:
                st.session_state.model_regressions_df = (
                    st.session_state.model_regressions_df.set_index("Test name")
                )
            st.session_state.model_regressions_df = (
                st.session_state.model_regressions_df.sort_values(
                    "r_squared", ascending=False
                )
            )
            st.subheader(
                f"Regression outputs for {st.session_state.y_sel_l[5:]} "
                f"\n All combinations of independent (x) variables ({st.session_state.n_counter+1} tests), "
                f"\n sorted by adjusted r squared highest to lowest"
            )
            with st.expander("Regression outputs"):
                # after test filtering is applied
                if st.session_state.model_regressions_filtered is not None:
                    st.session_state.selected_regression = st.dataframe(
                        st.session_state.model_regressions_filtered, on_select="rerun"
                    )
                # before any filtering is applied on any of the columns
                else:
                    st.session_state.selected_regression = st.dataframe(
                        st.session_state.model_regressions_df, on_select="rerun"
                    )
                 # extract min/max in order to apply filtering
                regression_min = st.session_state.model_regressions_df.min()
                regressions_max = st.session_state.model_regressions_df.max()
                st.session_state.regressions_min_max_df = pd.DataFrame([regression_min,regressions_max])
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

        # use the test name entered above to find the parameters from the equivalent test


        # create a list of test to loop through and calculate all forecasts from
        if st.session_state.model_regressions_df is not None:
            st.session_state.test_list = st.session_state.model_regressions_df.index.to_list()
            try:
                st.session_state.y_sel = st.session_state.y_sel_l.split("l: ")[1]
            except IndexError:
                pass


            for test in st.session_state.test_list:
                if st.session_state.model_regressions_df is not None:
                    try:
                        coeff_df = pd.DataFrame(
                            st.session_state.model_regressions_df.loc[test]
                        ).transpose()
                        st.session_state.coeff_dict[test] = coeff_df
                    except KeyError:
                        st.write("")
                if (test is not None and st.session_state.regr_tests_and_cols_dict != {}):
                    #TODO: Convert the following into a function - calc_elast_df




                    st.session_state.bc_plot_df = backcast_df(st.session_state.df,st.session_state.r_df,test,
                                                              st.session_state.y_sel_l[3:],
                                                              st.session_state.regr_tests_and_cols_dict[test],
                                                              st.session_state.coeff_dict
                                                              )
                    # print(st.session_state.bc_plot_df)
                    # st.session_state.elast_dict[test] = elast_df

                    st.session_state.bc_dict[test] = st.session_state.bc_plot_df

            if st.session_state.reg_sel is not None:
                st.subheader("Regression coefficients for selected test")
                coeff_df = st.data_editor(st.session_state.coeff_dict[st.session_state.reg_sel], num_rows="dynamic")
                # st.session_state.coeff_dict[st.session_state.reg_sel] = coeff_df
                #TODO: run a function here that updates bc_df
                st.subheader('Derived equation from current regression test')
                with st.expander('Show regression equation'):
                    st.latex(fr'''
                                    \ln(\text Traffic_t) = {coeff_df['const'][0]:.2f}  + \epsilon_t
                                    ''')
                    for col in coeff_df.columns[:-2]:
                        if coeff_df[col][0]>0:
                            st.latex(rf'+ {coeff_df[col][0]:.2f}\;ln({col[5:]}_t)')
                            # st.latex(type(col))
                        elif coeff_df[col][0]<0:
                            st.latex(rf'{coeff_df[col][0]:.2f}\;ln({col[5:]}_t)')
                        else:
                            pass
                with st.expander('Show equation solved for traffic'):
                    st.latex(fr'''
                                                    Traffic_t = e^{{{coeff_df['const'][0]:.2f} + \epsilon_t}} 
                                                    ''')
                    for col in coeff_df.columns[:-2]:
                        if math.isnan(coeff_df[col][0]):
                            pass
                        else:
                            st.latex(rf'\cdot({col[5:]}_t)^{{{coeff_df[col][0]:.2f}}}')

                st.header("Backcast:")
                st.session_state.bc_plot_df = st.session_state.bc_dict[st.session_state.reg_sel]
                st.session_state.bc_plot_df = st.session_state.bc_plot_df[['Forecast y', st.session_state.y_sel_l[3:]]]
                fig = px.line(
                    st.session_state.bc_plot_df,
                    x=st.session_state.bc_plot_df.index,
                    y=st.session_state.bc_plot_df.columns,
                    title=f"Forecast on historic data of {st.session_state.y_sel}",
                    color_discrete_sequence=st.session_state.custom_colors
                )
                fig.update_layout(xaxis_title="Year", yaxis_title="Variable")
                st.plotly_chart(fig)
                with st.expander('Display underlying data'):
                    st.dataframe(st.session_state.bc_dict[st.session_state.reg_sel])

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
