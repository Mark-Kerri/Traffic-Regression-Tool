# Statistical Analysis Tool

This Python-based Streamlit application provides a user-friendly interface for performing multivariate regression analysis on time series data. It guides analysts through data input, exploration, model configuration, automated regression runs, results evaluation, and report generation, with a focus on understanding the impact of various independent variables.

## Key Features

*   **Interactive Web Interface**: Built with Streamlit for an intuitive user experience.
*   **Excel Template Generation**: Create and download a pre-formatted Excel template (`.xlsx`) to ensure consistent data input. Powered by `openpyxl`.
*   **Data Ingestion & Exploration**:
    *   Upload completed Excel data files.
    *   Filter data by time periods and select specific variables for analysis.
    *   Visualize data through interactive line charts (raw and base-100 indexed), year-on-year growth charts, and scatter matrices using Plotly.
*   **Data Preprocessing**:
    *   Automatic log transformation for variables defined as 'absolute' values.
    *   Calculation of growth rates for time series analysis.
    *   Handles 'percentage/value/dummy' type variables appropriately.
    *   Option to generate seasonality dummy variables (e.g., for months or quarters).
*   **Multivariate Regression Analysis**:
    *   Utilizes `statsmodels.api.OLS` for robust Ordinary Least Squares regression.
    *   Automated execution of regressions for all combinations of selected independent variables.
    *   User-configurable inclusion of a constant (intercept) term.
*   **Model Evaluation & Selection**:
    *   Ranks regression models based on Adjusted R-squared.
    *   Provides detailed statistical outputs for each model, including:
        *   Coefficients and t-statistics.
        *   Durbin-Watson statistic (for autocorrelation).
        *   Variance Inflation Factor (VIF) (for multicollinearity).
        *   Log-likelihood.
    *   Residual analysis (residuals vs. fitted values plots).
*   **Advanced Filtering**:
    *   Exclude specific combinations of independent variables from being modeled together.
    *   Filter regression results based on desired ranges for model parameters (coefficients, R-squared).
*   **Backcasting & Interpretation**:
    *   Calculates in-sample predicted values ("backcast") for the selected model.
    *   Visualizes actual vs. predicted values.
    *   Displays the derived regression equation in LaTeX format.
    *   Allows interactive editing of coefficients for the selected model to see immediate impact on the backcast.
*   **Comprehensive Reporting**:
    *   Export detailed analysis results to an Excel file (`.xlsx`) using `xlsxwriter` and `openpyxl`.
    *   The report includes all run regression parameters, detailed statistics for the selected model, diagnostic charts, and input data.

## Tech Stack

*   Python 3.8+
*   Streamlit
*   Pandas
*   NumPy
*   Statsmodels
*   Plotly
*   Openpyxl
*   Xlsxwriter

## Directory Structure

  ```bash
   TRAFFIC-REGRESSION-TOOL/
   ├── data/
   │ ├── reg_input/ # Folder for user-generated/example Excel input files
   │ │ └── (Example_Data_File.xlsx)
   │ └── utils/
   │ └── excel_template_v0.01.xlsx # Base template for Excel inputs
   ├── src/
   │ ├── apppages/
   │ │ ├── utils/
   │ │ │ ├── excel.py # Functions for Excel file creation and parsing
   │ │ │ └── streamlit_tools.py # Helper functions for Streamlit UI and data ops
   │ │ ├── create_input_template.py # Page for generating Excel template
   │ │ ├── introduction.py # App introduction page
   │ │ ├── outputs.py # Page for exporting results
   │ │ ├── read_inputs.py # Page for data loading and exploration
   │ │ └── regression_ranking_refactored.py # Core regression analysis page
   │ └── app.py # Main Streamlit application script
   ├── venv/ # Python virtual environment (typically in .gitignore)
   ├── .gitignore
   ├── README.md
   └── requirements.txt
   ```

## Getting Started

### Prerequisites

*   Python 3.8 or higher
*   `pip` (Python package installer)
*   Git (for cloning the repository)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Traffic-Regression-Tool.git # Replace with your actual repo URL
    cd Traffic-Regression-Tool
    ```

2.  **Create and activate a virtual environment** (recommended):
    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  **Run the Streamlit application:**
    Make sure your terminal is in the root directory of the project (`Traffic-Regression-Tool/`).
    ```bash
    streamlit run src/app.py
    ```

2.  **Open the application in your browser:**
    Streamlit will typically open the application automatically in your default web browser. If not, navigate to `http://localhost:8501`.

3.  Follow the on-screen instructions within the app to:
    *   Generate an input template (or use an existing one).
    *   Upload your data.
    *   Explore the data.
    *   Configure and run regression analyses.
    *   Evaluate model results and export outputs.

## Future Enhancements (Planned)

*   **Cross-Validation**: Implement techniques like k-fold cross-validation to assess out-of-sample model performance.
*   **Advanced Time Series Diagnostics**: Include more formal tests for stationarity (e.g., ADF) and more detailed residual autocorrelation plots (ACF/PACF).
*   **Support for Lagged Variables**: Allow users to easily include lagged versions of dependent and independent variables in models.
*   **More Advanced Models**: Potentially incorporate models that handle autocorrelation directly (e.g., ARIMAX, SARIMAX, GLSAR).

---
