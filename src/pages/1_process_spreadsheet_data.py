import streamlit as st
import pandas as pd
import plotly.express as px
from pages.utils.process_inputs import spreadsheet_to_df  # pylint: disable=import-error
from pages.utils.process_inputs import *
default_file_path_for_testing = r"C:\Fidias\Coding-related\Python\Traffic-Regression-Tool\data\reg_input\Development Test Data Regression Inputs.xlsx"

def main():
    st.set_page_config(page_title="Process spreadsheet data")
    st.sidebar.success(
        "In this page, the user uploads the data for review before any calculation is performed"
    )
    st.header("Upload a filled version of the template spreadsheet:")
    filename = st.text_input(
        "Enter the full file path (without quotes):",
        value=default_file_path_for_testing
    )

    if st.button("Read spreadsheet"):
        st.session_state.df, st.session_state.df_index = spreadsheet_to_df(filename)
    if  st.session_state.df is not None:
        st.session_state.slider_value = st.select_slider(
        "Choose the first point to be plotted",
        options=range(0,len(st.session_state.df)-1),on_change= visualise_data(st.session_state.df,st.session_state.slider_value),format_func=stringify)
    if st.button("Export csv"):
        st.session_state.df[st.session_state.slider_value:].to_csv(st.session_state.export_file_path)
if __name__ == "__main__":
    main()
