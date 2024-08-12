"""
Introduction Page.

This script functions as the home page of the app, describing its functions and structure.
"""

import streamlit as st


def main():
    """Run main function to render the Streamlit app introduction page."""
    st.title("Regression Analysis Tool")

    st.markdown(
        """
        ## Welcome to the Regression Analysis Tool

        This application is designed to streamline the process of running multivariate regression
        analysis on timeseries data. It enables analysts to work with multiple dependent and
        independent variables simultaneously, providing comprehensive insights through various
        visualisations and exportable tabular outputs.

        ### Page Structure:
        - **Page 1: Input Template:**
          This page allows you to generate an Excel input template for data entry. This template
          will help ensure that your data is in the correct format for analysis. If you already
          have a template, you can skip this step.

        - **Page 2: Data Exploration:**
          Here, you can load the completed template and visualise the data. This page is useful
          for exploring the data before running any regression analysis.

        - **Page 3: Regression Control:**
          On this page, you can specify the parameters for the regression analysis and review the
          initial results. This is where you start to see how well the independent variables explain
          the dependent variables.

        - **Page 4: Model Evaluation:**
          This page allows you to review the predictive power of the regression model against
          historical data. You can also fine-tune the elasticities as needed.

        - **Page 5: Curate Outputs:**
          Finally, this page lets you curate the outputs from the analysis, ready for use in further
          analysis or reporting. You can export these outputs in various formats.

        Navigate through the apppages to use the tool's functionalities and streamline your traffic
        demand forecasting process.
        """
    )


if __name__ == "__page__":
    main()
