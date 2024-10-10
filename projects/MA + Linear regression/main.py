import model 
import backtest

if __name__ == "__main__":
    start_date = '2015-01-01'
    end_date = '2023-01-01'
    ticker = '^NDX'  # Nasdaq 100 index
    
    # Fetch and prepare the data
    data = model.fetch(ticker, start=start_date, end=end_date)
    data = model.add_indicators(data)
    
    # Train the model
    model, X_test, y_test = model.train(data)
    
    final_capital, trade_log = backtest.test(data, model, X_test, y_test, threshold=0.01, TP=0.05, SL=0.03)
    
    print(f"Final capital after backtest: {final_capital}")
    print(f"Trade log: {trade_log}")
