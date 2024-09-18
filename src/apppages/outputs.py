import streamlit as st
from apppages.utils.excel import export_to_excel,reformat_excel
import pandas as pd
def main():
    st.header('Export outputs')
    # st.text(st.session_state.reg_sel)
    df = st.session_state.model_regressions_df.iloc[st.session_state.selected_regression['selection']['rows']]
    output_summary_df = st.dataframe(df, on_select="rerun")
    tests = df.index
    st.session_state.output_path = st.text_input('Type the output folder path below:',value='outputs')


    forecast_df = pd.DataFrame()

    if st.button('Export output spreadsheet with selected regression'):
        r_df = st.session_state.log_df[st.session_state.slider_value_start:st.session_state.slider_value_end + 1]
        for test in tests:
            
            coeff_df_orig = df.loc[test]
            residuals_df = pd.DataFrame()
            summary_df = st.session_state.regression_rank_dict[test]
            residuals_df['Residuals'] = st.session_state.reg_residuals[test]
            residuals_df['Fitted values'] = st.session_state.reg_fitted_vals[test]
            residuals_df['Actuals'] = residuals_df['Residuals'] + residuals_df['Fitted values']
            # to be updated when each bc_df is saved in a dictionary  for each test?
            forecast_df = st.session_state.bc_dict[test]
            # st.text(st.session_state.bc_df)

            full_output_path = export_name = export_to_excel(st.session_state.model_regressions_df,r_df,test,coeff_df_orig,summary_df,residuals_df,st.session_state.output_path,forecast_df)
        # export_to_excel(coeff_df,df,reg_summary,residuals_df,path)
            reformat_excel(full_output_path,test)
if __name__ == "__page__":
    main()
