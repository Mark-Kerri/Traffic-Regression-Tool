import streamlit as st
from excel_editor import create_input_template


def main():
    st.title("Traffic Demand Forecasting Tool")

    # User input for independent variables
    independent_vars = st.text_area(
        "Enter Independent Variables (comma-separated)"
    ).split(",")

    if st.button("Generate Input Template"):
        output_path = "input_template.xlsx"
        create_input_template(independent_vars, output_path)
        st.success("Template Created Successfully!")
        st.download_button(
            label="Download Input Template",
            data=open(output_path, "rb").read(),
            file_name="input_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


if __name__ == "__main__":
    main()
