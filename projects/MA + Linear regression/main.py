import datetime
import model
import backtest  
import backtrader as bt

if __name__ == '__main__':
    # Define backtesting parameters
    ticker = 'AAPL'
    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime(2022, 1, 1)

    data = model.fetch(ticker, start=start_date, end=end_date)
    data = model.add_indicators(data)
    
    trained_model, X_test, y_test = model.train(data)

    # Prepare data for Backtrader
    data_bt = bt.feeds.PandasData(dataname=data)

    #Cerebro is backtrader's engine
    cerebro = bt.Cerebro()

    cerebro.addstrategy(backtest.PredictiveStrategy, model=trained_model)
    cerebro.adddata(data_bt)


    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.001)  # 0.1% commission per trade

    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

    cerebro.plot()
