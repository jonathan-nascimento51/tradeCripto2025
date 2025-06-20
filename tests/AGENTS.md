 Test Script Guidelines

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