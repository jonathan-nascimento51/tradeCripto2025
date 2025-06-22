# Test Script Guidelines

Each helper library inside `../libraries/` must have a corresponding `*_test.pine` file here under `tests/`.
These test scripts demonstrate the basic usage of the library and help confirm that exported functions work as expected.

## Writing Tests

- Keep each test minimal and self‑contained. Avoid external dependencies beyond the library under test.
- Include brief comments describing what should appear on the chart after running the script ("expected output").
- Use the naming convention `<library_name>_test.pine` so it is easy to locate the test for any given library.

## Loading Tests in TradingView

1. Open the **Pine Editor** in TradingView and create a new blank script.
2. Copy the contents of one of the `tests/*.pine` files into the editor.
3. Save and add the script to your chart. The comments in the file will indicate the expected visual result.

Following these steps keeps validation simple and ensures every library remains covered by a quick example.

## Opening Specific Tests

Load any `tests/*.pine` file using the steps above. Each one demonstrates a single library in isolation. After adding the script to your chart, confirm the library works by checking the visual cues below:

- `logistic_model_test.pine` – training loss plotted and a green **PASS** label when weights remain unchanged.
- `pivot_utils_test.pine` – triangle markers appear on pivot highs and lows.
- `sr_zone_utils_test.pine` – zone fills blue on retests and turns red when broken.
- `sr_manager_lib_test.pine` – a red zone appears at every new pivot high.
- `confluence_lib_test.pine` – line plot of the confluence weight and an alert if the weight scheme is invalid.
- `fib_extension_lib_test.pine` – standard Fibonacci extensions from the first bar.
- `fibo_projector_test.pine` – projection levels and an ATR-based golden zone near the last bars.
- `conf_box_lib_test.pine` – a single box is drawn then cleared on the last bar.
- `style_lib_test.pine` – close series uses the resistance color from `style_lib`.
- `fib_confluence_engine_test.pine` – gradient boxes highlight clustered Fibonacci levels.
- `combined_indicators_test.pine` – Fibonacci levels and SR zones draw from pivots; a logistic probability line oscillates between 0 and 1.
- `array_utils_lib_test.pine` – label shows the last value before clearing and `-1` on the final bar.
- `bucketing_lib_test.pine` – orange labels mark bucket counts for groups with at least two levels.
- `matrix_utils_lib_test.pine` – labels show "2" and "-1" on the first bar and "done" on the last.
- `price_precision_lib_test.pine` – first bar label lists mintick, raw and rounded prices; "Done" appears on the last bar.

### Prerequisites

- TradingView account with Pine Script V6 enabled.
- Any chart and timeframe works (1H BTCUSDT is recommended in the README).
- No external datasets or paid features are required.

## Checklist for New Libraries

1. Place the library under `libraries/` and declare it with `library("<Name>", true)`.
2. Keep implementation around 300 lines for clarity.
3. Add a matching `tests/<library_name>_test.pine` illustrating its usage.
4. Include a `// Expected output:` comment describing what should appear on the chart.
5. Run the test in TradingView and ensure no runtime errors occur.
6. Update this guide with the new test description if needed.
7. Commit using the prefix `agent::<nome>` as outlined in the repository guidelines.
