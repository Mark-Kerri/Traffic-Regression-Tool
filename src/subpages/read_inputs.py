import streamlit as st
from subpages.utils.process_inputs import (
    spreadsheet_to_df,
)  # pylint: disable=import-error
from subpages.utils.process_inputs import visualise_data
from subpages.utils.process_inputs import stringify, show_df

default_file_path_for_testing = r"C:\Fidias\Coding-related\Python\Traffic-Regression-Tool\data\reg_input\Development Test VKM Data Regression Inputs.xlsx"


def main():
    st.set_page_config(page_title="Process spreadsheet data")
    st.sidebar.success(
        "In this page, the user uploads the data for review before any calculation is performed"
    )
    st.header("Upload a filled version of the template spreadsheet:")
    filename = st.text_input(
        "Enter the full file path (without quotes):",
        value=default_file_path_for_testing,
    )

    if st.button("Read spreadsheet"):
        st.session_state.df, st.session_state.df_index, st.session_state.var_dict = (
            spreadsheet_to_df(filename)
        )
    if st.session_state.df is not None:
        st.session_state.slider_value_start, st.session_state.slider_value_end = (
            st.select_slider(
                "Choose the range of points to be plotted",
                options=range(0, len(st.session_state.df)),
                value=(0, len(st.session_state.df) - 1),
                # on_change=visualise_data,
                args=(
                    st.session_state.df,
                    st.session_state.slider_value_start,
                    st.session_state.slider_value_end,
                ),
                format_func=stringify,
            )
        )

        x_cols = [x for x in st.session_state.df.columns if x[0] == "x"]
        y_cols = [y for y in st.session_state.df.columns if y[0] == "y"]
        st.session_state.y_sel = st.selectbox(
            "Choose the dependent (endogenous) variable:", options=y_cols
        )
        st.session_state.x_sel = st.multiselect(
            "Choose independent (exogenous) variables:",
            options=x_cols,
            # on_change=show_df,
            args=(
                st.session_state.df[
                    st.session_state.slider_value_start : st.session_state.slider_value_end
                ],
                st.session_state.x_sel,
                st.session_state.y_sel,
            ),
        )
        if st.button("Preview dataframe"):
            show_df(
                st.session_state.df[
                    st.session_state.slider_value_start : st.session_state.slider_value_end
                    + 1
                ],
                st.session_state.x_sel,
                st.session_state.y_sel,
            )
            visualise_data(
                st.session_state.df,
                st.session_state.slider_value_start,
                st.session_state.slider_value_end,
            )
    # if st.button("Export csv"):
    #     st.session_state.df[st.session_state.slider_value_start:st.session_state.slider_value_end].to_csv(st.session_state.export_file_path)


if __name__ == "__page__":
    main()
