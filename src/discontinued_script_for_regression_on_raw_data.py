import pandas as pd
import numpy as np
import statsmodels.api as sm

# Sample quarterly data
data = {
    'Year': [2018, 2018, 2018, 2018, 2019, 2019, 2019, 2019],
    'Quarter': [1, 2, 3, 4, 1, 2, 3, 4],
    'GDP': [1000, 1020, 1010, 1050, 1080, 1100, 1150, 1200],
    'Traffic': [200, 204, 203, 210, 215, 220, 225, 230]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Log transform the GDP and Traffic columns
df['log_GDP'] = np.log(df['GDP'])
df['log_Traffic'] = np.log(df['Traffic'])

# Create dummy variables for the quarters
df = pd.get_dummies(df, columns=['Quarter'], drop_first=True)

# Set up the independent variables (log_GDP and quarter dummies)
X = df[['log_GDP', 'Quarter_2', 'Quarter_3', 'Quarter_4']]

# Add a constant (intercept) to the model
X = sm.add_constant(X)

# Set up the dependent variable (log_Traffic)
y = df['log_Traffic']

# Fit the log-log regression model with seasonality
model = sm.OLS(y, X).fit()

# Print the summary of the model
print(model.summary())
