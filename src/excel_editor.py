from openpyxl import load_workbook
from openpyxl.utils import get_column_letter


# Function to create the input template
def create_input_template(independent_vars, output_path):
    # Load the base template
    wb = load_workbook("base_template.xlsx")
    ws = wb.active

    # Set headers for independent variables
    for i, var in enumerate(independent_vars, start=3):
        col_letter = get_column_letter(i)
        ws[f"{col_letter}1"] = var

    # Save the modified template
    wb.save(output_path)
