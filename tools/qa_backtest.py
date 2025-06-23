import argparse
import json
import os
from itertools import product
from typing import Dict, List, Tuple, Any

import numpy as np
import pandas as pd
import requests


def run_tradingview_backtest(
    script_path: str,
    params: Dict[str, Any],
    start: str,
    end: str,
    api_key: str,
    simulate: bool = False,
) -> pd.DataFrame:
    """Execute a backtest via TradingView's API or return simulated results.

    Parameters
    ----------
    script_path : str
        Path to the Pine Script file.
    params : Dict[str, Any]
        Strategy parameters to optimize.
    start, end : str
        ISO formatted datetime strings bounding the test window.
    api_key : str
        TradingView API key.
    simulate : bool, optional
        If True or no API key is provided, returns random trades.
    """
    if simulate or not api_key:
        rng = np.random.default_rng()
        count = rng.integers(5, 20)
        data = {
            "timestamp": pd.date_range(start=start, periods=count, freq="H"),
            "profit": rng.normal(loc=10, scale=50, size=count),
        }
        return pd.DataFrame(data)

    base = os.environ.get("TRADINGVIEW_API_BASE", "https://api.tradingview.com")
    url = f"{base}/backtest"
    payload = {
        "script": open(script_path, "r", encoding="utf-8").read(),
        "params": params,
        "start": start,
        "end": end,
        "api_key": api_key,
    }
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    return pd.DataFrame(resp.json().get("trades", []))


def calculate_metrics(trades: pd.DataFrame) -> Dict[str, float]:
    """Compute common backtest metrics from a trades dataframe."""
    if trades.empty:
        return {"win_rate": 0.0, "profit_factor": 0.0, "max_drawdown": 0.0}
    equity = trades["profit"].cumsum()
    wins = trades["profit"] > 0
    win_rate = float(wins.mean())
    gross_profit = trades.loc[wins, "profit"].sum()
    gross_loss = abs(trades.loc[~wins, "profit"].sum())
    profit_factor = float(gross_profit / gross_loss) if gross_loss else float("inf")
    drawdown = (equity.cummax() - equity).max()
    return {
        "win_rate": round(win_rate, 4),
        "profit_factor": round(profit_factor, 4),
        "max_drawdown": round(float(drawdown), 4),
    }


def optimize_parameters(
    script_path: str,
    param_grid: Dict[str, List[Any]],
    start: str,
    end: str,
    api_key: str,
    simulate: bool = False,
) -> Dict[str, Any]:
    """Simple grid search returning params with highest net profit."""
    best_params: Dict[str, Any] = {}
    best_profit = -np.inf
    keys = list(param_grid.keys())
    for combo in product(*param_grid.values()):
        params = dict(zip(keys, combo))
        trades = run_tradingview_backtest(script_path, params, start, end, api_key, simulate)
        profit = trades["profit"].sum()
        if profit > best_profit:
            best_profit = profit
            best_params = params
    return best_params


def walk_forward(
    data: pd.DataFrame,
    script_path: str,
    param_grid: Dict[str, List[Any]],
    insample: int,
    outsample: int,
    api_key: str,
    simulate: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """Perform walk‑forward optimization over the dataset."""
    start = 0
    segments: List[pd.DataFrame] = []
    while start + insample + outsample <= len(data):
        insample_slice = data.iloc[start:start + insample]
        oos_slice = data.iloc[start + insample:start + insample + outsample]
        params = optimize_parameters(
            script_path,
            param_grid,
            insample_slice.index[0].isoformat(),
            insample_slice.index[-1].isoformat(),
            api_key,
            simulate,
        )
        trades = run_tradingview_backtest(
            script_path,
            params,
            oos_slice.index[0].isoformat(),
            oos_slice.index[-1].isoformat(),
            api_key,
            simulate,
        )
        segments.append(trades)
        start += outsample
    all_trades = pd.concat(segments, ignore_index=True) if segments else pd.DataFrame()
    metrics = calculate_metrics(all_trades)
    return all_trades, metrics


def _resample_array(values: np.ndarray) -> np.ndarray:
    rng = np.random.default_rng()
    idx = rng.integers(0, len(values), size=len(values))
    return values[idx]


def monte_carlo_analysis(trades: pd.DataFrame, iterations: int = 1000) -> Dict[str, Dict[str, float]]:
    """Run multiple Monte Carlo simulations on the trade list."""
    profits = trades["profit"].to_numpy()
    results = {"shuffle": [], "resample": [], "drop": []}
    rng = np.random.default_rng()
    for _ in range(iterations):
        shuffled = rng.permutation(profits)
        resampled = _resample_array(profits)
        mask = rng.random(len(profits)) > 0.1
        dropped = profits[mask]
        for label, arr in zip(
            ["shuffle", "resample", "drop"], [shuffled, resampled, dropped]
        ):
            df = pd.DataFrame({"profit": arr})
            results[label].append(calculate_metrics(df)["profit_factor"])
    summary: Dict[str, Dict[str, float]] = {}
    for key, arr in results.items():
        vals = np.array(arr)
        ci_low, ci_high = np.percentile(vals, [2.5, 97.5])
        summary[key] = {
            "mean": float(vals.mean()),
            "ci_low": float(ci_low),
            "ci_high": float(ci_high),
        }
    return summary


def save_results(
    script_name: str,
    metrics: Dict[str, float],
    distributions: Dict[str, Dict[str, float]],
    path: str = "benchmarks/advanced_backtests.json",
) -> None:
    """Persist metrics and distribution summaries under benchmarks/."""
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data[script_name] = {"metrics": metrics, "distributions": distributions}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file with OHLC data indexed by datetime."""
    df = pd.read_csv(path, parse_dates=[0])
    df.set_index(df.columns[0], inplace=True)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TradingView WFO backtests")
    parser.add_argument("script", help="Pine script to test")
    parser.add_argument("data", help="CSV price data")
    parser.add_argument("--api-key", default="", help="TradingView API key")
    parser.add_argument("--insample", type=int, default=500, help="IS window size")
    parser.add_argument("--outsample", type=int, default=100, help="OOS window size")
    parser.add_argument(
        "--grid",
        nargs="*",
        default=[],
        help="Parameter grid e.g. len=5,10 step=1,2",
    )
    parser.add_argument("--simulate", action="store_true", help="Skip API calls")
    args = parser.parse_args()

    grid: Dict[str, List[Any]] = {}
    for item in args.grid:
        key, values = item.split("=")
        grid[key] = [float(v) for v in values.split(",")]

    data = load_csv(args.data)
    trades, metrics = walk_forward(
        data,
        args.script,
        grid,
        args.insample,
        args.outsample,
        args.api_key,
        args.simulate,
    )
    dist = monte_carlo_analysis(trades)
    save_results(os.path.basename(args.script), metrics, dist)
    print(json.dumps({"metrics": metrics, "distributions": dist}, indent=2))


if __name__ == "__main__":
    main()
