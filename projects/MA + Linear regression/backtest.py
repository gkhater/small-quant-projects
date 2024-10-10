import backtrader as bt


class MyStrategy(bt.Strategy):
    params = (
        ('risk_percent', 0.005),   # 0.5% risk per trade
        ('rr_ratio', 2.5),         # 2.5:1 risk-reward ratio
        ('tp_factor', 0.9),        # Take profit at 90% of the predicted move
    )

    