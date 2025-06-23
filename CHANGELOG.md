# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Fixed exporting array constant in `fib_extension_lib.pine` and
  updated scripts to use color constants directly with `input.color`.
- Added feedback correction circuit with incident reports and regression prompt template.
- Added **FibConfluenceEngine** library for clustering Fibonacci levels and highlighting confluence zones.
- Fixed sorting logic in `clusterLevels()` to ensure compatibility with Pine Script's
  supported `array.sort` signature.
- Added **FiboProjector** library with ATR-based Golden Zone and a new test script.
- Added baseline metrics for `combined_indicators.pine` and `support_resistance_logistic_regression_example.pine` in `benchmarks/backtests.json`.
- Bumped Prompt-Builder to **v2.0** with a new `<backtest_and_validate>` action
  that instructs `qa_backtest` to run walk-forward optimization and Monte Carlo
  analyses whenever backtesting is requested.
- Added **RiskManager** library implementing Kelly-based position sizing with stop helpers.
- `fibo_projector.pine` now supports an adaptive golden zone via the new
  `useAdaptiveGZ` and `kFactor` parameters and has a demo toggle in
  `fibo_projector_test.pine`.

## [v2.0.0] - 2025-06-20
### Added
- **ConfluenceLib**: new library to compute confluence weights between Fibonacci and support/resistance levels.
- **logistic_model_lib**: replaced previous logistic regression utilities with a unified helper library.
- **Visual refinements**: introduced a consistent theme via `style_lib` and new box helpers for better chart readability.

## [v1.0.0] - 2025-05-01
### Added
- Initial set of support/resistance and pivot utilities.
- Example scripts demonstrating Fibonacci extensions and logistic regression zones.
