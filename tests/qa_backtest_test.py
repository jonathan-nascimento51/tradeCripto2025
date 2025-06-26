import os
import sys

import pandas as pd

try:
    from tools import qa_backtest as qb
except ImportError:  # Allows running without adjusting PYTHONPATH
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from tools import qa_backtest as qb


def test_walk_forward_and_monte_carlo() -> None:
    """Verify walk-forward backtesting and MC analysis run without error."""

    dates = pd.date_range("2022-01-01", periods=60, freq="h")
    df = pd.DataFrame(
        {"open": 1, "high": 1, "low": 1, "close": 1},
        index=dates,
    )

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

    # Basic assertions about the returned data
    assert not trades.empty
    assert set(metrics.keys()) == {"win_rate", "profit_factor", "max_drawdown"}

    mc = qb.monte_carlo_analysis(trades, iterations=10)
    assert {"shuffle", "resample", "drop"} <= set(mc.keys())
    for stats in mc.values():
        assert {"mean", "ci_low", "ci_high"} <= stats.keys()
