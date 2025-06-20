# tradeCripto2025

This repository contains example Pine Script V6 indicators. The new `ConfluenceLib` library provides a utility to calculate confluence weights between overlapping support/resistance and Fibonacci levels.

## ConfluenceLib
`ConfluenceLib.pine` exposes two user defined types, `ConfluenceInput` and `CalculatedWeights`, together with the `calculateConfluence()` function. The score combines multiple factors:

- `distance` – price distance between the two levels
- `signalStrength` – strength of the original signal (0..1)
- `retests` – number of times the level has been retested
- `temporalDiff` – difference in bars between the signals

Each component is multiplied by its respective coefficient before being summed into the final score.

## Recent Updates

- Logistic model expanded to consider volume as a third feature.
- Support/resistance probabilities now increase slightly on each retest (configurable).

```pinescript
import "./libraries/confluence_lib.pine" as conf
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
The file `examples/confluence_example.pine` shows how to detect simple support/resistance levels and Fibonacci retracements, compute confluence weights for overlapping levels and output them on the chart. Example JSON-like configuration

```json
{
  "distanceCoeff": 1.0,
  "signalCoeff": 1.2,
  "retestCoeff": 0.8,
  "temporalCoeff": 0.5
}
```

Load `examples/confluence_example.pine` on a chart and adjust the inputs to experiment with different weights.
The library now supports three weighting schemes: `linear`, `exponential` and `logistic`. When using the exponential mode the distance and temporal components are calculated as `exp(-k * value)` where `k` is configurable via the indicator inputs.
## Main Scripts

### `examples/combined_indicators.pine`
Located in the project root, this script demonstrates how to combine the logistic regression support/resistance model with Fibonacci extensions. It imports the helper libraries and plots both systems on the same chart.

### `examples/SupportandResistanceLogisticRegression.pine`
Standalone version of the logistic regression support/resistance indicator used inside `combined_indicators.pine`.

### `examples/confluence_example.pine`
Located in the project root, this minimal example shows how to detect support/resistance levels and Fibonacci retracements then calculate the confluence weight between them.

## Helper Libraries

### `libraries/pivot_utils.pine`
Small wrappers around `ta.pivothigh` and `ta.pivotlow` used to detect swing highs and lows.


### `libraries/sr_zone_utils.pine`
Common utilities for managing support/resistance zones (adding, clearing, retest and break logic).

### `libraries/logistic_model_lib.pine`
Combines the logistic function, log-loss and gradient descent training in a single module.

### `libraries/StyleLib`
Centralizes all default colors and chart styling options so indicators share the same visual theme. The library exposes `getStyles()` which returns an object with predefined color settings.

## Using the Libraries

1. In TradingView, create a new **Library** script and paste the contents of one of the `*_utils.pine` files. Save it with the exact name specified in the `library()` call (e.g. `Codex/PivotUtils/2`).
2. In your indicator or strategy, import the library with the `import` statement:

   ```pinescript
   import "./libraries/pivot_utils.pine" as pv
   ```

3. To keep a consistent color scheme, import `StyleLib` and retrieve the predefined styles:

   ```pinescript
   import "./libraries/style_lib.pine" as st
   st.Styles styles = st.getStyles()
   plot(close, color=styles.mainColor)
   ```

   Repeat the process for the other libraries as needed. Once imported you can call their exported functions directly in your scripts.

## Ajustes Visuais e Customização
- Agora é possível parametrizar a largura dos boxes de confluência através do input "Confluence Box Width" no indicador. Essa mudança visa melhorar a adaptação visual conforme o perfil do ativo.
