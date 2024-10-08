import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Fetch historical stock data for Apple (NAS100)
data = yf.download('^NDX', start='2015-01-01', end='2023-01-01')

# Display the first few rows of the data
print(data.head())

# Calculate the 50-day and 200-day moving averages
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['200_MA'] = data['Close'].rolling(window=200).mean()

# Calculate daily returns (percentage change in price)
data['Returns'] = data['Close'].pct_change()

# Drop rows with missing values (NaN)
data = data.dropna()

# Display the first few rows of the updated data
print(data.head())

# Define features (X) and target (y)
X = data[['50_MA', '200_MA', 'Returns']]
y = data['Close'].shift(-1)  # Predicting the next day's closing price

# Drop the last row as it will have NaN value for the target
X = X[:-1]
y = y[:-1]

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate the Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Plot the actual vs predicted stock prices
plt.figure(figsize=(10,6))
plt.plot(y_test.index, y_test, label='Actual Prices')
plt.plot(y_test.index, y_pred, label='Predicted Prices')
plt.title('Predicted vs Actual Stock Prices')
plt.legend()
plt.show()
