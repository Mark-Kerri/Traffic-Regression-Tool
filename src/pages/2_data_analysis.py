import pandas as pd
import streamlit as st
def main():
    st.set_page_config(page_title="Linear Regression setup")
    # initialize_session_state()
    st.sidebar.success(
        "In this page, the user will define the parameters/setup for the linear regressions"
    )
    st.header("Data preview:")
    # df = pd.read_csv(st.session_state.export_file_path)
    if st.session_state.df is not None:
        st.dataframe(data=st.session_state.df)
    else:
        st.write('No data is loaded. Use the previous page to load the input data.')


if __name__ == "__main__":
    main()