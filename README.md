# tradeCripto2025

This repository contains example Pine Script V6 indicators. The new `ConfluenceLib` library provides a utility to calculate confluence weights between overlapping support/resistance and Fibonacci levels.

## ConfluenceLib
`ConfluenceLib.pine` exposes two user defined types, `ConfluenceInput` and `CalculatedWeights`, together with the `calculateConfluence()` function. The score combines multiple factors:

- `distance` – price distance between the two levels
- `signalStrength` – strength of the original signal (0..1)
- `retests` – number of times the level has been retested
- `temporalDiff` – difference in bars between the signals

Each component is multiplied by its respective coefficient before being summed into the final score.

```pinescript
import ConfluenceLib as conf
inputData = conf.ConfluenceInput.new(fibLevel,
                                     srLevel,
                                     srProbability,
                                     atr,
                                     fibBar,
                                     srRetests,
                                     targetRetests,
                                     srBar,
                                     1.0,  // distance threshold
                                     50,   // max temporal difference
                                     1.0,  // distance coefficient
                                     1.0,  // signal strength coefficient
                                     1.0,  // retest coefficient
                                     1.0)  // temporal difference coefficient
conf.CalculatedWeights result = conf.calculateConfluence(inputData)
score = result.confluence_weight

## Example
`ConfluenceExample.pine` shows how to detect simple support/resistance levels and Fibonacci retracements, compute confluence weights for overlapping levels and output them on the chart. Example JSON-like configuration for the coefficients:

```json
{
  "distanceCoeff": 1.0,
  "signalCoeff": 1.2,
  "retestCoeff": 0.8,
  "temporalCoeff": 0.5
}
```

Load `ConfluenceExample.pine` on a chart and adjust the inputs to experiment with different weights.

## Main Scripts

### `autoFib-extension.pine`
Automatically draws Fibonacci extension levels using a zigzag based pivot search. The indicator exposes many inputs to customize which Fibonacci ratios are displayed and whether the lines extend left or right.

### `combined_indicator.pine`
Demonstrates how to combine the logistic regression support/resistance model with Fibonacci extensions. It imports the helper libraries and plots both systems on the same chart.

### `SupportandResistanceLogisticRegression.pine`
Full implementation of a logistic regression approach to support and resistance detection. It classifies pivots, plots the resulting zones and can generate alerts when retests or breaks occur.

## Helper Libraries

### `pivot_utils.pine`
Small wrappers around `ta.pivothigh` and `ta.pivotlow` used to detect swing highs and lows.

### `fibonacci_utils.pine`
Contains a utility to draw common Fibonacci extension levels between two prices.

### `logistic_regression_utils.pine`
Provides a logistic function and log-loss calculation used by the indicators.

## Using the Libraries

1. In TradingView, create a new **Library** script and paste the contents of one of the `*_utils.pine` files. Save it with the exact name specified in the `library()` call (e.g. `Codex/PivotUtils/1`).
2. In your indicator or strategy, import the library with the `import` statement:

   ```pinescript
   import Codex/PivotUtils/1 as pv
   ```

   Repeat the process for the other libraries as needed. Once imported you can call their exported functions directly in your scripts.
