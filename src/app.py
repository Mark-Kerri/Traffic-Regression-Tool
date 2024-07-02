import streamlit as st
import pandas as pd
from excel_editor import create_input_template  # pylint: disable=import-error


def initialize_session_state():
    if "y_vars" not in st.session_state:
        st.session_state.y_vars = {}
    if "x_vars" not in st.session_state:
        st.session_state.x_vars = {}


def main():
    initialize_session_state()

    st.title("Excel Template Generator")

    # Collect name variables
    st.header("Project Information")
    client = st.text_input("Client Name")
    project = st.text_input("Project Name")

    # Collect y variables
    st.header("Dependent Variables")
    y_var_name = st.text_input("Dependent Variable Name", key="y_name")
    y_var_type = st.selectbox("Dependent Variable Type", ["abs", "pct"], key="y_type")
    if st.button("Add Dependent Variable"):
        if y_var_name:  # Only add if name is not empty
            st.session_state.y_vars[y_var_name] = y_var_type
            st.success(f"Added dependent variable: {y_var_name}")

    # Display current y variables
    if st.session_state.y_vars:
        st.write("Current Dependent Variables:")
        st.write(
            pd.DataFrame(
                list(st.session_state.y_vars.items()), columns=["Variable", "Type"]
            )
        )

    # Collect x variables
    st.header("Independent Variables")
    x_var_name = st.text_input("Independent Variable Name", key="x_name")
    x_var_type = st.selectbox("Independent Variable Type", ["abs", "pct"], key="x_type")
    if st.button("Add Independent Variable"):
        if x_var_name:  # Only add if name is not empty
            st.session_state.x_vars[x_var_name] = x_var_type
            st.success(f"Added independent variable: {x_var_name}")

    # Display current x variables
    if st.session_state.x_vars:
        st.write("Current Independent Variables:")
        st.write(
            pd.DataFrame(
                list(st.session_state.x_vars.items()), columns=["Variable", "Type"]
            )
        )

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

    # Create button to generate Excel
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
            create_input_template(
                name_variables,
                st.session_state.y_vars,
                st.session_state.x_vars,
                timeline_inputs,
            )
            st.success("Excel template generated successfully!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
