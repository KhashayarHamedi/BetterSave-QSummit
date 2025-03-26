import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('365_day_predictions.csv')

# Divide the specified column by 10000
df['Predicted_Energy_Surplus'] = df['Predicted_Energy_Surplus'] / 10000

# Optionally, save the modified DataFrame back to a CSV file
df.to_csv('365_day_predictionsb.csv', index=False)
