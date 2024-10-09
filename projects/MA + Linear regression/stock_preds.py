import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2023, 1, 1)
# Fetch historical stock data for NAS 
data = yf.download('^NDX', start=start, end=end)

print(data.head())

# Calculate the 50-day and 200-day moving averages
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['200_MA'] = data['Close'].rolling(window=200).mean()

# Calculate percentage change in price
data['Returns'] = data['Close'].pct_change()

# Drop rows with missing values (NaN)
#i.e first column of Returns and n-1 columns of MA
data = data.dropna()

print(data.head())

# Define features (X) and target (y)
X = data[['50_MA', '200_MA', 'Returns']]
y = data['Close'].shift(-1)  # Predicting the next day's closing price

#We don't have data for the next day
X = X[:-1]
y = y[:-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Since this is my first project I want it to be simple, which is why I chose Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

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
