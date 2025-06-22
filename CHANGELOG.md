# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Fixed exporting array constant in `fib_extension_lib.pine` and
  updated scripts to use color constants directly with `input.color`.
- Added feedback correction circuit with incident reports and regression prompt template.
- Added **FibConfluenceEngine** library for clustering Fibonacci levels and highlighting confluence zones.
- Fixed sorting logic in `clusterLevels()` to ensure compatibility with Pine Script's
  supported `array.sort` signature.

## [v2.0.0] - 2025-06-20
### Added
- **ConfluenceLib**: new library to compute confluence weights between Fibonacci and support/resistance levels.
- **logistic_model_lib**: replaced previous logistic regression utilities with a unified helper library.
- **Visual refinements**: introduced a consistent theme via `style_lib` and new box helpers for better chart readability.

## [v1.0.0] - 2025-05-01
### Added
- Initial set of support/resistance and pivot utilities.
- Example scripts demonstrating Fibonacci extensions and logistic regression zones.