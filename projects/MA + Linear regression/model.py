import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

"""
fetches the data for a specific ticker from start to end
cleans up this data by dropping any NaN values
"""
def fetch(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    
    data = data.dropna()
    return data

"""
Adds 50 and 200 MAs for data
Also add daily pct change and RSI 
"""
def add_indicators(data):
    # Calculate 50-day and 200-day moving averages
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()

    # Calculate percentage change (returns)
    data['Returns'] = data['Close'].pct_change()

    # Calculate RSI (Relative Strength Index)
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Drop rows with NaN values generated from technical indicators
    data = data.dropna()
    return data


"""
Trains the model using an 80-20 test split
Using Linear Regression for simplicity (this is my first project)
"""
def train(data):
    X = data[['50_MA', '200_MA', 'Returns', 'RSI']]
    y = data['Close'].shift(-1)  # Predict next day's price

    # Drop the last row since we won't have a target for the last day
    X = X[:-1]
    y = y[:-1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, X_test, y_test


