"""
Introduction Page.

This script functions as the home page of the app, describing its functions and structure.
"""

import streamlit as st


def main():
    """Run main function to render the Streamlit app introduction page."""
    st.title("Statistical Analysis Tool")

    st.markdown(
        """
        ## Welcome to the Statistical Analysis Tool

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

        - **Page 3: Regression Ranking & Evaluation:**
          On this page, you define parameters to automatically run and rank
          multiple regression models. You can then review detailed statistics, compare models,
          and select the most suitable one for your analysis. This page then allows you to
          review the predictive power of the selected regression model against historical data.
          You can also fine-tune the elasticities (coefficients) as needed and see the impact.

        - **Page 4: Outputs:**
          Finally, this page lets you curate and export the outputs from the selected analysis,
          ready for use in further analysis or reporting.

        Navigate through the pages using the sidebar to use the tool's functionalities
        and streamline your forecasting process.
        """
    )


if __name__ == "__page__":
    main()
