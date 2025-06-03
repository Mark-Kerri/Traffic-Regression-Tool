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

from calendar import month_abbr
import streamlit as st
from apppages.utils.excel import create_input_template  # pylint: disable=import-error


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
    st.sidebar.info(
        "This page takes inputs from the user to generate an empty Excel Template file"
    )

    # Collect project information
    st.header("Project Information")
    client = st.text_input("Client Name")
    project = st.text_input("Project Name")

    # Collect dependent variables (Y variables)
    st.header("Dependent Variables")
    y_var_name = st.text_input("Dependent Variable Name", key="y_name")
    y_var_type = st.selectbox(
        "Dependent Variable Type",
        ["value", "dummy"],
        key="y_type",
    )
    if st.button("Add Dependent Variable"):
        if y_var_name and y_var_name not in st.session_state.y_vars:
            st.session_state.y_vars[y_var_name] = y_var_type
            st.success(f"Added dependent variable: {y_var_name}")
        elif y_var_name in st.session_state.y_vars:
            st.warning(f"Variable {y_var_name} already exists.")
        else:
            st.warning("Please enter a variable name.")

    # Display current dependent variables with delete buttons
    if st.session_state.y_vars:
        st.write("Current Dependent Variables:")
        for var_name, var_type in st.session_state.y_vars.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(var_name)
            with col2:
                st.write(var_type)
            with col3:
                if st.button("Delete", key=f"del_y_{var_name}"):
                    delete_x_y_variable("y", var_name)
                    st.rerun()

    # Collect independent variables (X variables)
    st.header("Independent Variables")
    x_var_name = st.text_input("Independent Variable Name", key="x_name")
    x_var_type = st.selectbox(
        "Independent Variable Type",
        ["value", "dummy"],
        key="x_type",
    )
    if st.button("Add Independent Variable"):
        if x_var_name and x_var_name not in st.session_state.x_vars:
            st.session_state.x_vars[x_var_name] = x_var_type
            st.success(f"Added independent variable: {x_var_name}")
        elif x_var_name in st.session_state.x_vars:
            st.warning(f"Variable {x_var_name} already exists.")
        else:
            st.warning("Please enter a variable name.")

    # Display current independent variables with delete buttons
    if st.session_state.x_vars:
        st.write("Current Independent Variables:")
        for var_name, var_type in st.session_state.x_vars.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(var_name)
            with col2:
                st.write(var_type)
            with col3:
                if st.button("Delete", key=f"del_x_{var_name}"):
                    delete_x_y_variable("x", var_name)
                    st.rerun()

    # Collect timeline inputs
    st.header("Timeline Information")
    timestep = st.selectbox("Timestep", ["Monthly", "Quarterly", "Yearly"])
    start_year = st.number_input(
        "Start Year", min_value=1900, max_value=2100, value=2012
    )
    end_year = st.number_input("End Year", min_value=1900, max_value=2100, value=2023)

    # Adjust start_timestep and end_timestep based on timestep
    if timestep == "Monthly":
        start_timestep = st.number_input(
            "Start Month", min_value=1, max_value=12, value=1
        )
        end_timestep = st.number_input("End Month", min_value=1, max_value=12, value=12)
    elif timestep == "Quarterly":
        start_timestep = st.number_input(
            "Start Quarter", min_value=1, max_value=4, value=1
        )
        end_timestep = st.number_input("End Quarter", min_value=1, max_value=4, value=4)
    else:  # Yearly
        start_timestep = 1
        end_timestep = 1
        st.write(
            "For yearly timestep, start and end timesteps are automatically set to 1."
        )

    # Collect output file name
    file_name = st.text_input(
        "Enter the file name (without quotes):", value=f"{project} Regression Inputs"
    )

    # define seasonality here
    # seas_bool_default = timestep == "Monthly" or timestep == "Quarterly"
    # seas_bool = st.checkbox("Add seasonality variables?",value=seas_bool_default)
    prd = st.session_state.prd_dict[timestep]
    if st.button(
        f"Generate seasonality variables for all "
        f"{timestep.replace('ly','').lower() if timestep else 'timestep'}s"
    ):
        if timestep == "Quarterly":
            for i in range(prd):
                st.session_state.x_vars["Q" + str(i + 1) + " Seasonality"] = "dummy"
            st.rerun()
        if timestep == "Monthly":
            for i in range(1, prd + 1):
                st.session_state.x_vars[month_abbr[i] + " Seasonality"] = "dummy"
            st.rerun()
        st.warning(
            f"Please remove the reference "
            f"{timestep.replace('ly','').lower() if timestep else 'timestep'}"
            f" from the seasonality variables list above",
            icon="⚠️",
        )

    # Button to generate Excel template
    if st.button("Generate Excel Template"):
        name_variables = {"Client": client, "Project": project}
        timeline_inputs = {
            "Timestep": timestep,
            "Start Year": start_year,
            "Start Timestep": start_timestep,
            "End Year": end_year,
            "End Timestep": end_timestep,
        }

        try:
            input_template = create_input_template(
                name_variables,
                st.session_state.y_vars,
                st.session_state.x_vars,
                timeline_inputs,
                file_name,
            )
            st.success("Excel template generated successfully!")

            st.download_button(
                label="Download Excel file",
                data=input_template,
                file_name=f"{file_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        except FileNotFoundError as fnf_error:
            st.error(f"File not found error: {fnf_error}")

        except ValueError as val_error:
            st.error(f"Value error: {val_error}")

        except PermissionError as perm_error:
            st.error(
                f"Permission error: {perm_error}. "
                "Check if you have the right permissions for the output directory."
            )

    # Button to switch page to next step
    if st.button("Next Page"):
        st.switch_page("apppages/read_inputs.py")


if __name__ == "__page__":
    main()
