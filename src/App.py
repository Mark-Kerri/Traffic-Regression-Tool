"""
Regression Analysis Tool.

This module implements a Streamlit-based web application designed to streamline the process of
running multivariate regression analysis on timeseries data. The tool allows analysts to define
multiple dependent and independent variables, visualise data, review initial regression results,
and evaluate the model's predictive power.

Key Features:
- **Excel Template Creation**: Generate an Excel input template to ensure the data is structured
  correctly for analysis.
- **Data Exploration**: Load and explore data from the Excel template to gain initial insights
  before running regression analysis.
- **Regression Parameter Definition**: Specify and adjust the parameters for the regression model,
  and review the initial analysis results.
- **Model Evaluation**: Evaluate how well the regression model predicts historical data and
  fine-tune elasticities as needed.
- **Output Curation**: Curate and export the desired outputs for further analysis and reporting.

The application consists of multiple subpages, each dedicated to a specific stage in the regression
analysis process. The page structure is designed to guide the user through the entire workflow from
data input to output curation.

Module Functions:
- `initialise_session_state()`: Initialises all session state variables required for the app's
  functionality.
- `main()`: The main function that initialises the app interface, including titles and introductory
  markdown.

Usage:
This module is meant to be executed as a standalone Streamlit application. When run, it will open a
web interface that guides users through the regression analysis process step-by-step.

"""

import streamlit as st


def initialise_session_state():
    """Initialise session state variables for managing data and app configurations."""
    if "y_vars" not in st.session_state:
        st.session_state.y_vars = {}
    if "x_vars" not in st.session_state:
        st.session_state.x_vars = {}
    if "inputs_file_path" not in st.session_state:
        st.session_state.inputs_file_path = None
    if "slider_value_start" not in st.session_state:
        st.session_state.slider_value_start = 0  # Default value
    if "slider_value_end" not in st.session_state:
        st.session_state.slider_value_end = -1  # Default value
    if "export_file_path" not in st.session_state:
        st.session_state.export_file_path = (
            "outputs/interim_df_output.csv"  # Default value
        )
    if "df" not in st.session_state:
        st.session_state.df = None
    if "df_index" not in st.session_state:
        st.session_state.df_index = None
    if "g_df_idx" not in st.session_state:
        st.session_state.g_df_idx = None
    if "var_dict" not in st.session_state:
        st.session_state.var_dict = {}
    if "prd_dict" not in st.session_state:
        st.session_state.prd_dict = {"Monthly": 12, "Quarterly": 4, "Yearly": 12}
    if "y_sel" not in st.session_state:
        st.session_state.y_sel = []
    if "x_sel" not in st.session_state:
        st.session_state.x_sel = []
    if "y_sel_g" not in st.session_state:
        st.session_state.y_sel_g = []
    if "x_sel_g" not in st.session_state:
        st.session_state.x_sel_g = []
    if "g_df" not in st.session_state:
        st.session_state.g_df = None
    if "r_df" not in st.session_state:
        st.session_state.r_df = None
    if "bc_df" not in st.session_state:
        st.session_state.bc_df = None
    if "bc_plot_df" not in st.session_state:
        st.session_state.bc_plot_df = None
    if "model_params" not in st.session_state:
        st.session_state.model_params = []


def main():
    """Run main function to render the Streamlit app interface."""
    initialise_session_state()

    introduction = st.Page(
        "subpages/introduction.py",
        title="Introduction",
        icon=":material/home:",
        default=True,
    )
    input_template = st.Page(
        "subpages/create_input_template.py",
        title="Create Input Template",
        icon=":material/edit_document:",
    )
    read_inputs = st.Page(
        "subpages/read_inputs.py", title="Data Exploration", icon=":material/analytics:"
    )
    regression = st.Page(
        "subpages/regression.py",
        title="Regression Control",
        icon=":material/stacked_line_chart:",
    )
    backcast = st.Page(
        "subpages/backcast.py", title="Model Evaluation", icon=":material/troubleshoot:"
    )
    outputs = st.Page("subpages/outputs.py", title="Outputs", icon=":material/output:")

    pg = st.navigation(
        [introduction, input_template, read_inputs, regression, backcast, outputs]
    )
    pg.run()


if __name__ == "__main__":
    main()
