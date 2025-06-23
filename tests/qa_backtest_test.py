import pandas as pd

# Allow direct execution without modifying PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools import qa_backtest as qb

if __name__ == "__main__":
    # Generate a small dummy dataset
    dates = pd.date_range("2022-01-01", periods=60, freq="H")
    df = pd.DataFrame({"open": 1, "high": 1, "low": 1, "close": 1}, index=dates)

    param_grid = {"len": [5, 10]}

    trades, metrics = qb.walk_forward(
        df,
        "dummy.pine",
        param_grid,
        insample=30,
        outsample=10,
        api_key="",
        simulate=True,
    )
    print("Trades", len(trades))
    print("Metrics", metrics)
    mc = qb.monte_carlo_analysis(trades, iterations=50)
    print("MC", mc["shuffle"]["mean"])
