import backtrader as bt
import pandas as pd

class PredictiveStrategy(bt.Strategy):
    params = (('model', None),)  # Accept the model as a parameter

    def __init__(self):
        self.predicted_price = None  # Store the predicted price
        self.order = None  # Keep track of open orders
        self.bar_open = 1e9  # To track the bar when the position was opened
        self.risk = 0.01

        # Create indicators for moving averages, returns, and RSI (To match those calculated in the model)
        self.ma_50 = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.ma_200 = bt.indicators.SimpleMovingAverage(self.data.close, period=200)
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data.close, period=14)
        self.returns = bt.indicators.RateOfChange(self.data.close, period=1)

    def next(self):
        # Prepare the input for prediction
        features = pd.DataFrame({
            'MA_50': [self.ma_50[0]],
            'MA_200': [self.ma_200[0]],
            'Returns': [self.returns[0]],
            'RSI': [self.rsi[0]]
        })

        # Predict next day price using the model
        self.predicted_price = self.params.model.predict(features)[0]

        anticipated_move = self.predicted_price - self.data.close[0]
        
        min_move_threshold = 0.005  # This is the minimum treshhold for us to buy/sell


        cash_available = self.broker.getcash()
        # Position sizing
        position_size = cash_available * self.risk / self.data.close[0]  

        # Trade logic: if move is big enough place TP at 90% of expected move and SL such that RR = 2.5
        #NOTE: I know this isn't a sound trading strategy, I'm just learning syntax
        if not self.position and abs(anticipated_move) > min_move_threshold:
            if self.predicted_price > self.data.close[0]:
                # Buy order: set TP and SL
                buy_price = self.data.close[0]
                tp = buy_price + anticipated_move * 0.90  # Take profit at 90% of the anticipated move
                sl = buy_price - (anticipated_move / 2.5)  # Stop loss based on 2.5 risk/reward
                self.order = self.buy_bracket(size=position_size, limitprice=tp, stopprice=sl)
                self.bar_open = len(self)  # Record the bar at which the position is opened (This will be used later)
            elif self.predicted_price < self.data.close[0]:
                # Sell order: set TP and SL
                sell_price = self.data.close[0]
                tp = sell_price - anticipated_move * 0.90  # Take profit at 90% of the anticipated move
                sl = sell_price + (anticipated_move / 2.5)  # Stop loss based on 2.5 risk/reward
                self.order = self.sell_bracket(size=position_size, limitprice=tp, stopprice=sl)
                self.bar_open = len(self)  # Record the bar at which the position is opened (This will be used later)

        # Time-based exit logic: close after 1 day (assuming 1 bar = 1 day)
        if self.position:
            if len(self) - self.bar_open >= 2:  # Close after 1 day (2 bars: current and next day)
                self.close()
                self.bar_open = 1e9  # Reset bar_open after closing
