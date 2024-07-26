import streamlit as st
from pages.utils.excel_editor import create_input_template  # pylint: disable=import-error


def initialize_session_state():
    if "y_vars" not in st.session_state:
        st.session_state.y_vars = {}
    if "x_vars" not in st.session_state:
        st.session_state.x_vars = {}
    if 'slider_value' not in st.session_state:
        st.session_state.slider_value = 0  # Default value
    if 'export_file_path' not in st.session_state:
        st.session_state.export_file_path = 'data/interim_output.csv'  # Default value
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'df_index' not in st.session_state:
        st.session_state.df_index = None

def delete_variable(var_type, var_name):
    if var_type == "y":
        del st.session_state.y_vars[var_name]
    else:
        del st.session_state.x_vars[var_name]


def main():
    st.set_page_config(page_title="Generate Excel Template file")
    initialize_session_state()
    st.sidebar.success(
        "This page takes inputs from the user to generate an empty Excel Template file"
    )

    # Collect name variables
    st.header("Project Information")
    client = st.text_input("Client Name")
    project = st.text_input("Project Name")

    # Collect y variables
    st.header("Dependent Variables")
    y_var_name = st.text_input("Dependent Variable Name", key="y_name")
    y_var_type = st.selectbox("Dependent Variable Type", ["abs", "pct_change","pct_val_or_dummy"], key="y_type")
    if st.button("Add Dependent Variable"):
        if y_var_name and y_var_name not in st.session_state.y_vars:
            st.session_state.y_vars[y_var_name] = y_var_type
            st.success(f"Added dependent variable: {y_var_name}")
        elif y_var_name in st.session_state.y_vars:
            st.warning(f"Variable {y_var_name} already exists.")
        else:
            st.warning("Please enter a variable name.")

    # Display current y variables with delete buttons
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
                    delete_variable("y", var_name)
                    st.experimental_rerun()

    # Collect x variables
    st.header("Independent Variables")
    x_var_name = st.text_input("Independent Variable Name", key="x_name")
    x_var_type = st.selectbox("Independent Variable Type", ["abs", "pct_change","pct_val_or_dummy"], key="x_type")
    if st.button("Add Independent Variable"):
        if x_var_name and x_var_name not in st.session_state.x_vars:
            st.session_state.x_vars[x_var_name] = x_var_type
            st.success(f"Added independent variable: {x_var_name}")
        elif x_var_name in st.session_state.x_vars:
            st.warning(f"Variable {x_var_name} already exists.")
        else:
            st.warning("Please enter a variable name.")

    # Display current x variables with delete buttons
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
                    delete_variable("x", var_name)
                    st.experimental_rerun()

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
    output_folder_path = st.text_input(
        "Enter the folder path where the output file will be saved (without quotes):"
        )
    file_name = st.text_input(
        "Enter the file name (without quotes):"
        , value=f"{project} Regression Inputs")

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
                file_name,
                output_folder_path
            )
            st.success("Excel template generated successfully!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
