"""
Statistical Analysis Tool.

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

The application consists of multiple apppages, each dedicated to a specific stage in the regression
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
    default_states = {
        "y_vars": {},
        "x_vars": {},
        "inputs_file_path": None,
        "slider_value_start": 0,
        "slider_value_end": -1,
        "base_slider_value_start": 0,
        "base_slider_value_end": -1,
        "export_file_path": "outputs/interim_df_output.csv",
        "df": None,
        "g_df": None,
        "df_index": None,
        "g_df_idx": None,
        "l_df_idx": None,
        "var_dict": {},
        "timestep": None,
        "prd_dict": {"Monthly": 12, "Quarterly": 4, "Yearly": 1},
        "prd": None,
        "y_sel": [],  # General Y selection
        "x_sel": [],  # General X selection
        "y_sel_l": [],  # Log-transformed Y selection (likely for regression target)
        "x_sel_l": [],  # Log-transformed X selection (likely for regression predictors)
        "y_sel_g": [],  # Growth-transformed Y selection (if needed)
        "x_sel_g": [],  # Growth-transformed X selection (if needed)
        "x_sel_reg": [],  # X variables for a specific regression run
        "log_df": None,
        "l_df": None,  # Seems to be an alias or earlier version of log_df
        "r_df": None,  # Dataframe for regression
        "bc_df": None,  # Backcast dataframe
        "bc_plot_df": None,
        "model_params": [],  # This might be better as a dict if it stores params for one model
        "regression_outputs": {},
        "regr_tests_and_cols_dict": {},
        "model_r_squared": [],  # Might be better as part of regression_outputs
        "model_regressions_df": None,
        "model_regressions_filtered": None,
        "regressions_min_max_df": None,
        "model_regressions_list": None,  # List of regression test names
        "reg_sel": None,  # Selected regression test name
        "n_counter": 0,
        "constant_sel": False,
        "selected_regression": None,  # From dataframe selection event
        "reg_influence": None,
        "reg_residuals": {},
        "reg_fitted_vals": {},
        "residuals_df": None,
        "residuals_df_filtered": None,
        "output_path": None,  # Should this be a user input or a fixed path?
        "custom_colors": [
            "#009dc8",
            "black",
            "orange",
            "darkgreen",
            "blue",
            "darkred",
            "#A7C7E7",
        ],
        "coeff_dict": {},
        "coeff_df": None,  # Coeffs for a selected regression
        "elast_dict": {},
        "bc_dict": {},  # Dictionary to store backcast dataframes per test
        "test_list": None,
        "test_names_and_ids": {},
        "bc_plot_dict": {},
        "x_interaction_table": None,
        "x_inter_stack": None,
        "x_combos_to_exclude": None,
        "parameter_filters": None,
        "param_t": None,
    }

    for key, default_value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def main():
    """Run main function to render the Streamlit app interface."""
    initialise_session_state()

    introduction = st.Page(
        "apppages/introduction.py",
        title="Introduction",
        icon=":material/home:",
        default=True,
    )
    input_template = st.Page(
        "apppages/create_input_template.py",
        title="Input Template",
        icon=":material/edit_document:",
    )
    read_inputs = st.Page(
        "apppages/read_inputs.py",
        title="Data Exploration",
        icon=":material/analytics:",
    )
    regression_ranking_refactored = st.Page(
        "apppages/regression_ranking_refactored.py",
        title="Regression Ranking",
        icon=":material/stacked_line_chart:",
    )
    outputs = st.Page(
        "apppages/outputs.py",
        title="Outputs",
        icon=":material/output:",
    )

    pg = st.navigation(
        [
            introduction,
            input_template,
            read_inputs,
            regression_ranking_refactored,
            outputs,
        ]
    )
    pg.run()


if __name__ == "__main__":
    main()
