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
The file `example/confluence_example.pine` shows how to detect simple support/resistance levels and Fibonacci retracements, compute confluence weights for overlapping levels and output them on the chart. Example JSON-like configuration

```json
{
  "distanceCoeff": 1.0,
  "signalCoeff": 1.2,
  "retestCoeff": 0.8,
  "temporalCoeff": 0.5
}
```

Load `example/confluence_example.pine` on a chart and adjust the inputs to experiment with different weights.
The library now supports three weighting schemes: `linear`, `exponential` and `logistic`. When using the exponential mode the distance and temporal components are calculated as `exp(-k * value)` where `k` is configurable via the indicator inputs.
## Main Scripts

### `combined_indicators.pine`
Located in the project root, this script demonstrates how to combine the logistic regression support/resistance model with Fibonacci extensions. It imports the helper libraries and plots both systems on the same chart.

### `example/SupportandResistanceLogisticRegression.pine`
Standalone version of the logistic regression support/resistance indicator used inside `combined_indicators.pine`.

### `example/confluence_example.pine`
Located in the `example/` folder, this minimal example shows how to detect support/resistance levels and Fibonacci retracements then calculate the confluence weight between them.

## Helper Libraries

### `libraries/pivot_utils.pine`
Small wrappers around `ta.pivothigh` and `ta.pivotlow` used to detect swing highs and lows.


### `libraries/sr_zone_utils.pine`
Common utilities for managing support/resistance zones (adding, clearing, retest and break logic).

### `libraries/logistic_model_lib.pine`
This library replaces the older `logistic_regression_utils.pine` and `logistic_training_utils.pine` files.

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

## Library Test Scripts
To validate each helper library independently, open any of the files under `tests/` in the TradingView Pine editor.

1. **Load a test file**
   - In TradingView, open the **Pine Editor** and create a new blank script.
   - Copy the contents of one of the `tests/*.pine` files into the editor.
   - Save and add the indicator to the chart.
2. **Expected output**
   - `logistic_model_test.pine` plots the training loss of a toy dataset and shows a label with the probability for the first sample.
   - `pivot_utils_test.pine` draws triangle markers at detected pivot highs and lows.
   - `sr_zone_utils_test.pine` creates a demo zone on the first bar and updates its state when price retests or breaks it.
   - `sr_manager_lib_test.pine` adds a zone whenever a pivot high forms using the manager helper.
   - `confluence_lib_test.pine` plots the calculated confluence weight as a line.
   - `fib_extension_lib_test.pine` draws basic Fibonacci levels using the style defaults.
   - `conf_box_lib_test.pine` creates a single box and then clears it at the last bar.
   - `style_lib_test.pine` simply plots the close series using one of the palette colors.

Running these scripts helps confirm that each exported function executes without errors and produces visible output on the chart.