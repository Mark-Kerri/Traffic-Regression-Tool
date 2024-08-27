import streamlit as st
from apppages.utils.excel import export_to_excel
import pandas as pd
def main():
    st.header('Export outputs')
    df = st.session_state.model_regressions_df.iloc[st.session_state.selected_regression['selection']['rows']]
    output_summary_df = st.dataframe(df, on_select="rerun")
    tests = df.index
    st.session_state.output_path = st.text_input('Type the output folder path below:',value='outputs')


    # add plot from current selection only (TODO: need to create and save bc_plot_df from all tests?)
    forecast_df = st.session_state.bc_plot_df

    if st.button('Export output spreadsheet with selected regression'):
        for test in tests:
            residuals_df = pd.DataFrame()
            coeff_df = df.loc[test]
            summary_df = st.session_state.regression_rank_dict[test]
            residuals_df['Residuals'] = st.session_state.reg_residuals[test]
            residuals_df['Fitted values'] = st.session_state.reg_fitted_vals[test]
            residuals_df['Actuals'] = residuals_df['Residuals'] + residuals_df['Fitted values']
            # to be updated when each bc_df is saved in a dictionary  for each test?
            forecast_df = forecast_df
            export_to_excel(test,coeff_df,summary_df,residuals_df,st.session_state.output_path,forecast_df)
        # export_to_excel(coeff_df,df,reg_summary,residuals_df,path)

if __name__ == "__page__":
    main()
