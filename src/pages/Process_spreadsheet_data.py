import streamlit as st
import pandas as pd
import plotly.express as px
from process_inputs import spreadsheet_to_df  # pylint: disable=import-error


def visualize_data(df):
    df_idx = df.index
    df_x = pd.DataFrame(index=df_idx)
    df_y = pd.DataFrame(index=df_idx)

    # split x and y columns into separate dfs
    for col in df.columns:
        if col[0] == "x":
            df_x[col] = df[col]
        elif col[0] == "y":
            df_y[col] = df[col]

    # Scatter plot
    # for x in df_x.columns:
    #     for y in df_y.columns:
    # fig = px.scatter(df, x=x, y=y)
    # st.plotly_chart(fig)
    fig = px.line(df, x=df.index, y=df.columns)
    st.plotly_chart(fig)

    df_indexed = 100 * (df / df.iloc[0, :])
    fig = px.line(df_indexed, x=df_indexed.index, y=df_indexed.columns)
    st.plotly_chart(fig)

    # st.subheader("Basic Statistics")
    # st.write(df.describe())
    #
    # st.subheader("Matplotlib Visualization")
    # fig, ax = plt.subplots()
    # df.hist(ax=ax)
    # st.pyplot(fig)
    #
    # st.subheader("Seaborn Visualization")
    # fig, ax = plt.subplots()
    # sns.heatmap(df.corr(), annot=True, ax=ax)
    # st.pyplot(fig)
    #
    # st.subheader("Plotly Visualization")
    # fig = px.scatter_matrix(df)
    # st.plotly_chart(fig)


def main():
    st.set_page_config(page_title="Process spreadsheet data")
    # initialize_session_state()
    st.sidebar.success(
        "In this page, the user uploads the data for review before any calculation is performed"
    )
    st.header("Upload a filled version of the template spreadsheet:")
    filename = st.text_input(
        "Enter the filename (with extension) saved in data/reg_input folder:"
    )
    print(filename)
    if st.button("Read spreadsheet"):
        df = spreadsheet_to_df(filename)
        if df is not None:
            visualize_data(df)
    # uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls", "csv"])
    #
    # if uploaded_file is not None:
    #     try:
    #         # Check the file extension and read accordingly
    #         if uploaded_file.name.endswith('.csv'):
    #             df = pd.read_csv(uploaded_file)
    #         else:
    #             df = pd.read_excel(uploaded_file)
    #
    #         st.write("File Uploaded Successfully!")
    #         st.dataframe(df)  # Display the dataframe
    #
    #     except Exception as e:
    #         st.write(f"Error: {e}")


if __name__ == "__main__":
    main()
