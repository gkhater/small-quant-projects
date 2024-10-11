import datetime
import model
import backtest  # Import your strategy file
import backtrader as bt

if __name__ == '__main__':
    # Define backtesting parameters
    ticker = 'AAPL'
    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime(2022, 1, 1)

    # Fetch and prepare data
    data = model.fetch(ticker, start=start_date, end=end_date)

    data = model.add_indicators(data)
    # Train the model
    trained_model, X_test, y_test = model.train(data)

    # Prepare data for Backtrader
    data_bt = bt.feeds.PandasData(dataname=data)

    # Initialize Cerebro (Backtrader's engine)
    cerebro = bt.Cerebro()

    # Add the strategy with the trained model
    cerebro.addstrategy(backtest.PredictiveStrategy, model=trained_model)

    # Add the data feed
    cerebro.adddata(data_bt)

    # Set initial capital
    cerebro.broker.setcash(10000.0)

    # Set commission for trades
    cerebro.broker.setcommission(commission=0.001)  # 0.1% commission

    # Print starting portfolio value
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')

    # Run the backtest
    cerebro.run()

    # Print final portfolio value
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

    # Plot the results
    cerebro.plot()
