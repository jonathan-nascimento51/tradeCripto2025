# tradeCripto2025

This repository contains example Pine Script V6 indicators. The new `ConfluenceLib` library provides a utility to calculate confluence weights between overlapping support/resistance and Fibonacci levels.

## ConfluenceLib
`ConfluenceLib.pine` exposes a `WeightParams` type and a `calcWeight` function. The score combines multiple factors:

- `distance` – price distance between the two levels
- `signalStrength` – strength of the original signal (0..1)
- `retests` – number of times the level has been retested
- `temporalDiff` – difference in bars between the signals

Each component is multiplied by its respective coefficient before being summed into the final score.

```pinescript
import ConfluenceLib as conf
params = conf.WeightParams.new(distance,
                               signalStrength,
                               retests,
                               temporalDiff,
                               1.0,  // distance coefficient
                               1.0,  // signal strength coefficient
                               1.0,  // retest coefficient
                               1.0)  // temporal difference coefficient
score = conf.calcWeight(params)
```

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
