# tradeCripto2025

This repository hosts a small collection of Pine Script **v6** indicators for use on TradingView. The scripts are provided as study material for traders wanting to experiment with automatic Fibonacci extensions and support/resistance detection using logistic regression.

## Included indicators

- **autoFib-extension.pine** – automatically draws Fibonacci extension levels based on recent pivot highs and lows. It imports the built‑in `TradingView/ZigZag/7` library for pivot detection.
- **SupportandResistanceLogisticRegression.pine** – plots potential support and resistance zones using a simple logistic regression model.

## Loading the scripts in TradingView

1. Open [TradingView](https://www.tradingview.com/) and navigate to the **Pine Editor** tab.
2. Create a new script and paste the contents of the desired `.pine` file from this repository.
3. Click **Add to chart** (or **Save** if you only want to store the script).
4. Adjust the user inputs from the script’s settings panel to suit your chart and timeframe.

## Dependencies and assumptions

- The scripts require Pine Script version 6, which is available in modern TradingView editors.
- `autoFib-extension.pine` depends on TradingView’s public ZigZag library. This is imported automatically – no extra installation is necessary.
- No external data sources or libraries are used beyond those provided by TradingView.

## Basic usage and configuration

### Auto Fib Extension

1. Load `autoFib-extension.pine` as described above.
2. Set the **Depth** input to control how many bars are scanned for pivot points. Smaller depths find more recent swings, while larger depths find major pivots.
3. Toggle the individual Fibonacci levels (e.g., 0.382, 0.618) in the settings to customise what is displayed.
4. Reversing the levels or extending them left/right can be managed via the inputs.

### Support and Resistance Logistic Regression

1. Load `SupportandResistanceLogisticRegression.pine`.
2. Configure **Pivot Length** to specify how many bars define a significant high or low.
3. **Target Respects** determines how many retests of a level are needed before it is deemed strong. Higher values reduce noise.
4. **Probability Threshold** filters out low‑confidence levels from the logistic regression model. Raising it yields fewer, but more selective, zones.
5. Optional inputs allow hiding far lines or showing additional debugging labels. Alerts are included for retests and breaks of detected zones.

These scripts are examples only and should be tested thoroughly on different assets and timeframes before being used in live trading.
