import streamlit as st
from apppages.utils.excel import export_to_excel,reformat_excel
import pandas as pd
import os
def main():
    st.header('Export outputs')
    if st.session_state.model_regressions_df is not None:
        df = st.session_state.model_regressions_df.iloc[st.session_state.selected_regression['selection']['rows']]
        df_mod = df#.set_index('Test id')
        output_summary_df = st.dataframe(df_mod, on_select="rerun")
        df_t = df_mod.T

        tvalues_df = st.session_state.regression_outputs[st.session_state.reg_sel]['t stats']

        tests = df.index
        # st.session_state.output_path = st.text_input('Type the output folder path below:',value='outputs')
        tvalues_df = pd.DataFrame(tvalues_df)
        combined_df = pd.concat([df_t, tvalues_df], axis=0)
        combined_df.sort_index(inplace=True)
        st.dataframe(combined_df,on_select="rerun")
        # print(type(df_t))
        # print(type(tvalues_df))

        forecast_df = pd.DataFrame()

    if st.button('Export output spreadsheet with selected regression'):
        r_df = st.session_state.log_df[st.session_state.slider_value_start:st.session_state.slider_value_end + 1]
        for test in tests:
            
            coeff_df_orig = df.loc[test]
            residuals_df = pd.DataFrame()
            summary_df = st.session_state.regression_outputs[test]['model summary']
            residuals_df['Residuals'] = st.session_state.reg_residuals[test]
            residuals_df['Fitted values'] = st.session_state.reg_fitted_vals[test]
            residuals_df['Actuals'] = residuals_df['Residuals'] + residuals_df['Fitted values']
            # to be updated when each bc_df is saved in a dictionary  for each test?
            forecast_df = st.session_state.bc_dict[test]
            # st.text(st.session_state.bc_df)
            path = os.getcwd()
            buffer = export_to_excel(st.session_state.model_regressions_df,r_df,test,coeff_df_orig,summary_df,residuals_df,path,forecast_df)
        # export_to_excel(coeff_df,df,reg_summary,residuals_df,path)
            buffer = reformat_excel(buffer,test)
            # Create a download button for the user to download the Excel file
            st.download_button(
                label="Download Excel file",
                data=buffer,
                file_name=f"file_name.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
if __name__ == "__page__":
    main()
