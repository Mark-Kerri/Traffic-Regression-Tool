"""
Excel Template Generator for Regression Analysis.

This Streamlit module provides an interface for users to create an Excel template
for regression analysis. Users can define dependent and independent variables,
set project and timeline details, and then generate an Excel file for data input.

The main functions include:
- Collecting user inputs for project details, variables, and timeline information.
- Validating the output folder path and generating the Excel template.
- Displaying current variables and allowing the user to delete any unwanted variables.

Modules:
- pathlib: Used for handling filesystem paths.
- streamlit: Streamlit library to create the web-based user interface.
- apppages.utils.excel: Custom utility module to generate the Excel template.

"""

from calendar import month_abbr, month_name
import streamlit as st
from apppages.utils.excel import create_input_template


def delete_x_y_variable(var_type, var_name):
    """
    Delete a dependent or independent variable from session state.

    Parameters:
    - var_type (str): Type of the variable, either 'x' for independent or 'y' for dependent.
    - var_name (str): The name of the variable to be deleted.
    """
    if var_type == "y":
        del st.session_state.y_vars[var_name]
    else:
        del st.session_state.x_vars[var_name]


def main():
    """
    Run main function to render the Streamlit app interface.

    This function sets up the Streamlit UI, collects user inputs for the project,
    dependent and independent variables, timeline information, and allows the user
    to generate an Excel template file for regression analysis. The function also
    includes input validation and error handling to ensure correct execution.
    """
    st.title("Input Template")
    st.markdown(
        "Provide project and data information to create your Excel inputs template."
    )
    st.info(
        "**Note:** You can add/edit variables directly in the downloaded Excel template. "
        "However, defining the timeline (start/end dates, timestep) is best done using this tool"
        " before generating the template."
    )
    st.sidebar.info(
        "This page takes inputs from the user to generate an empty Excel Template file"
    )

    # --- Project Information ---
    st.header("Project Information")
    client = st.text_input("Client Name", key="client_name_input")
    project = st.text_input("Project Name", key="project_name_input")
    file_name = st.text_input(
        "Enter the file name for the template (without quotes):",
        value=f"{project} Regression Inputs" if project else "Regression Inputs",
        key="file_name_input",
    )
    st.markdown(
        "> _Tip: If you prefer to add most variables directly in Excel, you can "
        "generate the template with the default variables and edit them there. "
        "Defining the timeline here is still recommended._"
    )

    # --- Dependent Variables (Y variables) ---
    st.header("Dependent Variables")
    y_var_name = st.text_input("Dependent Variable Name", key="y_name_input")
    y_var_type = st.selectbox(
        "Dependent Variable Type",
        ["value", "dummy"],
        key="y_type_select",
    )

    col_add_y, col_clear_y = st.columns([1, 1])
    with col_add_y:
        if st.button("Add Dependent Variable", use_container_width=True):
            if y_var_name and y_var_name not in st.session_state.y_vars:
                st.session_state.y_vars[y_var_name] = y_var_type
                st.success(f"Added dependent variable: {y_var_name}")
            elif y_var_name in st.session_state.y_vars:
                st.warning(f"Variable {y_var_name} already exists.")
            else:
                st.warning("Please enter a variable name.")
    with col_clear_y:
        if st.button("Clear All Dependent Variables", use_container_width=True):
            st.session_state.y_vars = {}

    # Display current dependent variables
    if st.session_state.y_vars:
        st.write("Current Dependent Variables:")
        for var_name_disp, var_type_disp in st.session_state.y_vars.items():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(var_name_disp)
            with col2:
                st.write(var_type_disp)
            with col3:
                if st.button(
                    "Delete",
                    key=f"del_y_{var_name_disp.replace(' ', '_')}",
                    use_container_width=True,
                ):
                    delete_x_y_variable("y", var_name_disp)
                    st.rerun()

    # --- Independent Variables (X variables) ---
    st.header("Independent Variables")
    x_var_name = st.text_input("Independent Variable Name", key="x_name_input")
    x_var_type = st.selectbox(
        "Independent Variable Type",
        ["value", "dummy"],
        key="x_type_select",
    )

    col_add_x, col_clear_x = st.columns([1, 1])
    with col_add_x:
        if st.button("Add Independent Variable", use_container_width=True):
            if x_var_name and x_var_name not in st.session_state.x_vars:
                st.session_state.x_vars[x_var_name] = x_var_type
                st.success(f"Added independent variable: {x_var_name}")
            elif x_var_name in st.session_state.x_vars:
                st.warning(f"Variable {x_var_name} already exists.")
            else:
                st.warning("Please enter a variable name.")
    with col_clear_x:
        if st.button("Clear All Independent Variables", use_container_width=True):
            st.session_state.x_vars = {}

    # Display current independent variables
    if st.session_state.x_vars:
        st.write("Current Independent Variables:")
        for var_name_disp, var_type_disp in st.session_state.x_vars.items():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(var_name_disp)
            with col2:
                st.write(var_type_disp)
            with col3:
                if st.button(
                    "Delete",
                    key=f"del_x_{var_name_disp.replace(' ', '_')}",
                    use_container_width=True,
                ):
                    delete_x_y_variable("x", var_name_disp)
                    st.rerun()

    # --- Timeline Information ---
    st.header("Timeline Information")
    timestep = st.selectbox(
        "Timestep", ["Monthly", "Quarterly", "Yearly"], key="timestep_select"
    )

    month_options = list(month_name)[1:]  # Full names: January, February...

    col_start_year, col_start_period = st.columns(2)
    col_end_year, col_end_period = st.columns(2)

    with col_start_year:
        start_year = st.number_input(
            "Start Year",
            min_value=1900,
            max_value=2100,
            value=2010,
            key="start_year_input",
        )
    with col_end_year:
        end_year = st.number_input(
            "End Year", min_value=1900, max_value=2100, value=2025, key="end_year_input"
        )

    start_timestep_val = 1
    end_timestep_val = 1

    if timestep == "Monthly":
        with col_start_period:
            selected_start_month_name = st.selectbox(
                "Start Month",
                options=month_options,
                index=0,
                key="start_month_select",  # Default to January
            )
            start_timestep_val = (
                month_options.index(
                    selected_start_month_name
                    if selected_start_month_name
                    else "January"
                )
                + 1
            )
        with col_end_period:
            selected_end_month_name = st.selectbox(
                "End Month",
                options=month_options,
                index=11,
                key="end_month_select",  # Default to December
            )
            end_timestep_val = (
                month_options.index(
                    selected_end_month_name if selected_end_month_name else "December"
                )
                + 1
            )
    elif timestep == "Quarterly":
        with col_start_period:
            start_timestep_val = st.number_input(
                "Start Quarter", min_value=1, max_value=4, value=1, key="start_q_input"
            )
        with col_end_period:
            end_timestep_val = st.number_input(
                "End Quarter", min_value=1, max_value=4, value=4, key="end_q_input"
            )
    else:  # Yearly
        with col_start_period:
            st.write("")  # left blank
        with col_end_period:
            st.write("")  # left blank
        # start_timestep_val and end_timestep_val remain 1

    # --- Seasonality Generation Refined ---
    st.subheader("Seasonality Variables (Optional)")
    generate_seasonality_flag = st.checkbox(
        "Generate seasonality dummy variables?", key="gen_seas_flag"
    )
    reference_period_val = None

    if generate_seasonality_flag:
        if timestep == "Monthly":
            monthly_ref_options = list(month_abbr)[1:]
            reference_period_val = st.selectbox(
                "Select reference month to exclude:",
                options=monthly_ref_options,
                index=len(monthly_ref_options) - 1,  # Default to last month (e.g., Dec)
                key="ref_month_select",
            )
        elif timestep == "Quarterly":
            quarterly_ref_options = [f"Q{i+1}" for i in range(4)]
            reference_period_val = st.selectbox(
                "Select reference quarter to exclude:",
                options=quarterly_ref_options,
                index=len(quarterly_ref_options) - 1,  # Default to Q4
                key="ref_q_select",
            )
        else:  # Yearly
            st.write("Seasonality is not applicable for Yearly timestep.")

        if timestep in ["Monthly", "Quarterly"]:
            col_gen_seas, col_clear_seas = st.columns(2)
            with col_gen_seas:
                if st.button("Generate Seasonality Dummies", use_container_width=True):
                    current_x_vars = st.session_state.x_vars.copy()
                    if timestep == "Monthly":
                        prd = 12
                        for i in range(1, prd + 1):
                            month_short_name = month_abbr[i]
                            if month_short_name != reference_period_val:
                                current_x_vars[f"{month_short_name} Seasonality"] = (
                                    "dummy"
                                )
                    elif timestep == "Quarterly":
                        prd = 4
                        for i in range(prd):
                            q_name = f"Q{i+1}"
                            if q_name != reference_period_val:
                                current_x_vars[f"{q_name} Seasonality"] = "dummy"
                    st.session_state.x_vars = current_x_vars
                    st.success(
                        "Seasonality dummy variables generated (excluding reference)."
                    )
                    st.rerun()
            with col_clear_seas:
                if st.button("Clear Seasonality Dummies", use_container_width=True):
                    # More robustly find and remove seasonality variables
                    vars_to_remove = [
                        var_name
                        for var_name in st.session_state.x_vars
                        if "Seasonality" in var_name
                        and (
                            var_name.startswith("Q")
                            or any(m in var_name for m in list(month_abbr))
                        )
                    ]
                    for var_name_rem in vars_to_remove:
                        if var_name_rem in st.session_state.x_vars:
                            del st.session_state.x_vars[var_name_rem]
                    if vars_to_remove:
                        st.success("Seasonality dummy variables cleared.")
                        st.rerun()
                    else:
                        st.info("No seasonality dummy variables found to clear.")

    # --- Button to generate Excel template ---
    st.divider()
    if st.button("Generate Excel Template", type="primary", use_container_width=True):
        if not st.session_state.y_vars:
            st.session_state.y_vars["Default_Y_Variable"] = "value"
            st.info("Added a default Y variable as none were specified.")

        if not st.session_state.x_vars:
            st.session_state.x_vars["Default_X_Variable"] = "value"
            st.info("Added a default X variable as none were specified.")

        # Proceed only if both Y and X variables exist
        if st.session_state.y_vars and st.session_state.x_vars:
            name_variables = {"Client": client, "Project": project}
            timeline_inputs = {
                "Timestep": timestep,
                "Start Year": start_year,
                "Start Timestep": start_timestep_val,
                "End Year": end_year,
                "End Timestep": end_timestep_val,
            }

            try:
                input_template_buffer = create_input_template(
                    name_variables,
                    st.session_state.y_vars,
                    st.session_state.x_vars,
                    timeline_inputs,
                    file_name,
                )
                st.success("Excel template generated successfully!")

                st.download_button(
                    label="Download Excel file",
                    data=input_template_buffer,
                    type="primary",
                    use_container_width=True,
                    file_name=f"{file_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_template_btn",
                )

            except FileNotFoundError as fnf_error:
                st.error(f"Template file not found error: {fnf_error}")
            except ValueError as val_error:
                st.error(f"Value error: {val_error}")

    # --- Button to switch page to next step ---
    if st.button("Next Page", use_container_width=True):
        st.switch_page("apppages/read_inputs.py")


if __name__ == "__page__":
    main()
