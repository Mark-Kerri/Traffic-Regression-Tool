import streamlit as st
from apppages.utils.excel import export_to_excel
import pandas as pd
def main():
    st.header('Export outputs')
    st.text(st.session_state.reg_sel)
    df = st.session_state.model_regressions_df.iloc[st.session_state.selected_regression['selection']['rows']]
    output_summary_df = st.dataframe(df, on_select="rerun")
    tests = df.index
    st.session_state.output_path = st.text_input('Type the output folder path below:',value='outputs')


    # add plot from current selection only (TODO: need to create and save bc_plot_df from all tests?)
    forecast_df = st.session_state.bc_plot_df

    if st.button('Export output spreadsheet with selected regression'):
        g_df = st.session_state.g_df[st.session_state.slider_value_start:st.session_state.slider_value_end+1]
        for test in tests:
            
            coeff_df_orig = df.loc[test]
            reg_cols = st.session_state.regr_tests_and_cols_dict[
                test
            ]
            coeff_df = pd.DataFrame(
                    st.session_state.model_regressions_df.loc[test]
                ).transpose()            
            print(reg_cols)
            print(coeff_df[reg_cols])
            elast_df = (
                st.session_state.g_df[reg_cols] ** coeff_df[reg_cols].iloc[0][reg_cols]
            )
            st.session_state.bc_df = pd.DataFrame(
                data=elast_df.shift(periods=-st.session_state.prd),
                index=st.session_state.df.index,
            )
            st.session_state.bc_df["Combined Growth"] = 1  # None
            for col in reg_cols:
                st.session_state.bc_df.loc[
                    st.session_state.bc_df.index[-st.session_state.prd :], col
                ] = 1
            st.session_state.bc_df = st.session_state.bc_df.reset_index()

            st.session_state.bc_df["Predicted y"] = None
            st.session_state.bc_df["Forecasted y"] = None
            base_year_start = st.session_state.base_slider_value_start
            base_year_end = st.session_state.base_slider_value_end
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
                -st.session_state.prd
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



            residuals_df = pd.DataFrame()
            summary_df = st.session_state.regression_rank_dict[test]
            residuals_df['Residuals'] = st.session_state.reg_residuals[test]
            residuals_df['Fitted values'] = st.session_state.reg_fitted_vals[test]
            residuals_df['Actuals'] = residuals_df['Residuals'] + residuals_df['Fitted values']
            # to be updated when each bc_df is saved in a dictionary  for each test?
            forecast_df = st.session_state.bc_df[st.session_state.slider_value_start:st.session_state.slider_value_end+1+st.session_state.prd]
            forecast_df = forecast_df[["Forecasted y", st.session_state.y_sel]]

            base_year_datapoints = forecast_df.index[st.session_state.base_slider_value_start:st.session_state.base_slider_value_end+1+st.session_state.prd]

            # st.text(st.session_state.bc_df)

            export_to_excel(base_year_datapoints,g_df,test,coeff_df_orig,summary_df,residuals_df,st.session_state.output_path,forecast_df)
        # export_to_excel(coeff_df,df,reg_summary,residuals_df,path)

if __name__ == "__page__":
    main()
