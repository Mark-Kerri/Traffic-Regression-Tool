# Traffic-Regression-Tool
A Python-based tool to determine elasticities to input independent variables using multivariate regression analysis. This tool provides an easy-to-use interface for analysts to input data, configure model parameters, and obtain statistically significant traffic forecasts with detailed elasticity reports. This tool enables analysts to run regressions on traffic time series data against user-defined independent variables and generate detailed reports on the best-fit models and their elasticities.

## Features

- **User-Friendly Interface**: Easily input data and configure model parameters using a Streamlit-based web interface.
- **Excel Integration**: Generate and download customized Excel templates for data input, with robust handling and formatting powered by openpyxl.
- **Statistical Analysis**: Automatically identify and rank the best-fit models based on statistical significance.
- **Elasticity Calculation**: Determine the elasticity of traffic demand concerning each independent variable.
- **Cross-Validation**: Ensure model robustness with cross-validation techniques (planned for future sprints).
- **Advanced Visualization**: Visualize regression results and diagnostics with interactive plots (planned for future sprints).
- **Scalability**: Handle large datasets efficiently with distributed computing solutions (planned for future sprints).
- **Machine Learning Models**: Incorporate advanced ML models for improved prediction accuracy (planned for future sprints).

## Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/traffic-demand-forecasting-tool.git
   cd traffic-demand-forecasting-tool

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install the required packages:
   ```sh
   pip install -r requirements.txt

### Usage

1. Run the Streamlit app:
   ```sh
   streamlit run src/app.py

2. Open your web browser and navigate to http://localhost:8501.

3. Use the interface to input data, configure model parameters, and generate forecasts.

## Directory Structure

  ```sh
  traffic-demand-forecasting-tool/
  ├── data/                     # Sample data files
  ├── src/
  │   ├── __init__.py
  │   ├── data_processing.py    # Code for reading and processing input data
  │   ├── regression_analysis.py # Code for performing regression analysis
  │   ├── model_selection.py    # Code for selecting the best fit model
  │   ├── elasticity_calculation.py # Code for calculating elasticities
  │   ├── app.py                # Streamlit app code
  │   ├── utils.py              # Utility functions
  ├── tests/
  │   ├── test_data_processing.py
  │   ├── test_regression_analysis.py
  │   ├── test_model_selection.py
  │   ├── test_elasticity_calculation.py
  ├── requirements.txt          # List of dependencies
  ├── README.md
  └── Dockerfile                # Docker configuration


