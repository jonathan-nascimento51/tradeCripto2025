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
- New **RiskManager** library provides Kelly-based position sizing utilities.

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

### `example/support_resistance_logistic_regression_example.pine`
Standalone version of the logistic regression support/resistance indicator used inside `combined_indicators.pine`.

### `example/confluence_example.pine`
Located in the `example/` folder, this minimal example shows how to detect support/resistance levels and Fibonacci retracements then calculate the confluence weight between them.

## Helper Libraries

### `libraries/pivot_utils.pine`
Small wrappers around `ta.pivothigh` and `ta.pivotlow` used to detect swing highs and lows.

### `libraries/pivot_ring_buffer_lib.pine`
Stores potential pivot points in a ring buffer until enough bars have passed to confirm them. Useful when you want to defer validation and avoid premature repainting.

```pinescript
import "./libraries/pivot_ring_buffer_lib.pine" as prb

prb.RingBuffer rb = prb.newRingBuffer(20)
[float ph, float pl] = prb.processCandidate(rb, high, low, 3, 3)
// `ph` and `pl` hold values only after `rightBars` bars have elapsed
```

### `libraries/sr_zone_utils.pine`
Common utilities for managing support/resistance zones (adding, clearing, retest and break logic).

### `libraries/logistic_model_lib.pine`
This library replaces the older `logistic_regression_utils.pine` and `logistic_training_utils.pine` files.
`gradientDescent()` now accepts optional initial weights so training can resume from a previous state. When invalid input is detected the function issues an `alert()` instead of halting the script and the returned result sets `ok` to `false`.

### `libraries/StyleLib`
Centralizes all default colors and chart styling options so indicators share the same visual theme. The library exposes `getStyles()` which returns an object with predefined color settings.

### `libraries/fib_confluence_engine.pine`
Provides an engine for detecting pivot swings and deriving Fibonacci levels from
them. Levels that fall within a chosen distance are grouped into clusters so
zones of confluence can be highlighted on the chart. The library exports the
`Swing` and `Cluster` types along with `detectSwings()`, `getFibLevels()`,
`clusterLevels()` and `drawClusters()` helper functions.

Here is a short example that wires these helpers together:

```pinescript
import "./libraries/fib_confluence_engine.pine" as fce
import "./libraries/style_lib.pine" as st

st.Styles styles = st.getStyles()
var fce.Swing[] swings = array.new<fce.Swing>()
var box[] boxes = array.new<box>()

fce.detectSwings(swings, high, low, 5, 5)
[float[] levels, float[] weights] = fce.getFibLevels(swings)
fce.Cluster[] clusters = fce.clusterLevels(levels, weights, atr(14) * 0.25)
fce.drawClusters(clusters, boxes, bar_index - 30, bar_index, styles.fib_base_color)
```

See `tests/fib_confluence_engine_test.pine` for a minimal runnable script with the same logic.

### `libraries/fibo_projector.pine`
Computes Fibonacci projection levels from a pivot pair and highlights an adaptive
*Golden Zone*. The `Projector` type stores levels and offers
`computeLevels()` and `draw()` helpers. `computeLevels()` now accepts two
additional parameters:

- `useAdaptiveGZ` – when `true`, the golden zone is centered on the 50% level and
  sized using `kFactor * ATR`.
- `kFactor` – multiplier for ATR in the adaptive calculation.

When `useAdaptiveGZ` is `false`, the classic 1.618 projection zone sized by
`atrMult` remains available.

### `libraries/bucketing_lib.pine`
Provides `bucketMap()` to group nearby price levels into buckets rounded to the symbol's minimum tick.

### `libraries/risk_manager.pine`
Provides Kelly-based position sizing along with helpers for stop-loss and take-profit levels.

in the `library()` declaration (e.g. `PivotUtils` with version `2`).
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

### Importing Libraries on TradingView

When publishing a script that depends on a library, reference the public
version hosted by the author. Use the following syntax:

```pinescript
import username/libraryName/1 as lib
```

Replace `username` with the TradingView profile name, `libraryName` with the
library's published title and `1` with the desired version. Note that relative
paths like `"./libraries/pivot_utils.pine"` only work when running the files
inside this repository.

Both `combined_indicators.pine` and `support_resistance_logistic_regression_example.pine` keep the logistic model weights fixed unless the **Use Trained Weights** input is enabled. The coefficients may be entered manually or trained on‑the‑fly when this option is turned on.

## Ajustes Visuais e Customização
- Agora é possível parametrizar a largura dos boxes de confluência através do input "Confluence Box Width" no indicador. Essa mudança visa melhorar a adaptação visual conforme o perfil do ativo.

## Baseline de Backtest e Correção de Regressões
O repositório inclui o arquivo `benchmarks/backtests.json` com as métricas de referência para os principais scripts. O agente `qa_backtest` compara cada nova execução com esses valores e gera um relatório de incidente se o `Profit-factor` cair mais de 2 % abaixo do baseline. Esse relatório é utilizado pelo `prompt_builder` para criar um prompt de correção que será enviado ao `impl_codex`.

### Running a Simple Backtest

1. Abra `combined_indicators.pine` no editor Pine do TradingView.
2. Configure o gráfico para **BTCUSDT** em 1 hora e volte 180 dias.
3. Clique em **Add to Chart** dentro da aba *Strategy Tester* para executar o backtest.
4. Compare `Profit-factor`, `Win-rate` e `Max drawdown` com os valores de `benchmarks/backtests.json`.
5. Diferenças acima de ~2 % indicam regressão ou melhoria em relação ao baseline.

### Atualizando benchmarks

Para novas versões dos scripts, execute novamente o backtest com o mesmo período (BTCUSDT 1h, 180 dias). Copie os valores de **Win-rate**, **Profit-factor** e **Max drawdown** da aba *Strategy Tester* e substitua-os no arquivo `benchmarks/backtests.json`. Registre a atualização no `CHANGELOG.md` e faça o commit com o prefixo `agent::doc_writer`.

## Library Test Scripts
To validate each helper library independently, open any of the files under `tests/` in the TradingView Pine editor.

1. **Load a test file**
   - In TradingView, open the **Pine Editor** and create a new blank script.
   - Copy the contents of one of the `tests/*.pine` files into the editor.
   - Save and add the indicator to the chart.
2. **Expected output**
   - `logistic_model_lib_test.pine` plots the training loss of a toy dataset and shows a label with the probability for the first sample.
   - `pivot_utils_test.pine` draws triangle markers at detected pivot highs and lows.
   - `sr_zone_utils_test.pine` creates a demo zone on the first bar and updates its state when price retests or breaks it.
   - `sr_manager_lib_test.pine` adds a zone whenever a pivot high forms using the manager helper.
   - `confluence_lib_test.pine` plots the calculated confluence weight as a line.
   - `fib_extension_lib_test.pine` draws basic Fibonacci levels using the style defaults.
   - `fibo_projector_test.pine` shows projection levels and an ATR-based Golden Zone.
   - `conf_box_lib_test.pine` creates a single box and then clears it at the last bar.
   - `style_lib_test.pine` simply plots the close series using one of the palette colors.

Running these scripts helps confirm that each exported function executes without errors and produces visible output on the chart.
## Context Utilities
`tools/context_utils.py` provides small helper functions used by the prompt builder.
These allow building a compact "context pack" without reading entire files.

- `extract_code_snippet(file_path, function_name)` returns a slice of code around the
  target function so only relevant lines are included in the prompt.
- `extract_text_section(file_path, start_keyword, end_keyword)` extracts documentation
  between two keywords.
- `get_file_structure(directory)` lists files in a directory, giving a quick overview
  of the project layout.

## Automation Workflow
To streamline repository updates, the script `tools/auto_commit_push.py` automates
staging, committing and pushing changes.

### Usage
```bash
python tools/auto_commit_push.py "Fix typo" --agent impl_codex
```
This command stages all modifications, creates the commit `Fix typo – agent::impl_codex`
and pushes it to the current branch on the `origin` remote. Use `--files`, `--branch`
or `--remote` for finer control.

### Setting up a Remote
If you cloned the repository without specifying a remote, configure one before pushing:

```bash
git remote add origin <https://github.com/jonathan-nascimento51/tradeCripto2025>
git push -u origin main
```

`git push` will fail until a remote named `origin` (or the one you specify) is added.
### Manual Commit Example
```bash
git add AGENTS.md
git commit -m "Atualiza convencoes de commit – agent::doc_writer"
git push
```
Every commit should include the prefix `agent::<nome>` in the message and should not be amended to keep history intact.

## Python Requirements
The Python helper scripts and example tests depend on a few external packages. A
`requirements.txt` file lists them for convenience:

```
pandas
numpy
requests
flake8
```

Install everything with:

```bash
pip install -r requirements.txt
```

With the dependencies installed you can execute tools like
`tools/qa_backtest.py` or run the standalone test files under `tests/` without
import errors.

## Advanced Backtesting
The `tools/qa_backtest.py` script performs walk-forward optimization on CSV files exported manually from TradingView. There is no official API. To generate a dataset:

1. Abra o ativo e timeframe desejados em TradingView.
2. Selecione **Export chart data...** no menu do gráfico.
3. Salve o arquivo em `data/BTCUSD_1H.csv` (ou similar) e passe esse caminho para o script.

O script também executa simulações de Monte Carlo. Example usage:
```bash
python tools/qa_backtest.py combined_indicators.pine data/BTCUSD_1H.csv --grid len=5,10 step=1,2 --insample 500 --outsample 100 --simulate
```
Results are saved in `benchmarks/advanced_backtests.json` and include 95% confidence intervals.

### Configuring WFO Windows

Use `--insample` and `--outsample` to define the size of each walk‑forward window in bars. A longer in‑sample window generally produces more stable parameters while a smaller out‑of‑sample window offers more test cycles.

```bash
python tools/qa_backtest.py combined_indicators.pine data/BTCUSD_1H.csv \
  --grid len=20,50 step=1,2 \
  --insample 720 --outsample 240 \
  --simulate
```

The aggregated equity curve for all segments is written to `wfo_report.json`.

### Running Monte Carlo

After the walk‑forward run finishes, the script automatically performs Monte Carlo simulations on the generated trade list. The resulting statistics and confidence intervals are stored in `monte_carlo_stats.json` alongside the main metrics file.
## Contribution Guidelines

- Every commit message must begin with `agent::<nome>` as described in `AGENTS.md`.
- Avoid rewriting history with `git commit --amend`; create a new commit for each change.
