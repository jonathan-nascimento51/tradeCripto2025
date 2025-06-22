# Example Scripts Guidelines

This directory contains minimal Pine Script examples that showcase how to integrate the helper libraries provided in this repository. Use them as reference when creating your own indicators or tests.

## Purpose of Each Example

- **`autoFib-extension.pine`** – Demonstrates a basic Fibonacci extension tool without external libraries. It provides a starting point for converting standalone logic into reusable library functions.
- **`confluence_example.pine`** – Illustrates how to import `confluence_lib.pine` and `style_lib.pine` to calculate overlap between simple support/resistance levels and Fibonacci ranges. It highlights passing a `ConfluenceInput` object to `calculateConfluence()` and plotting the resulting score.
- **`SupportandResistanceLogisticRegression.pine`** – Shows a more complete integration of multiple libraries (`logistic_model_lib`, `sr_zone_utils`, `pivot_utils`, `sr_manager_lib` and `style_lib`). It manages zones, trains a logistic model on‑the‑fly and applies unified styles.

## Expected Chart Behaviour

1. **Auto Fib Extension** – Draws colored lines at each Fibonacci ratio from the last detected pivot range. You should see levels updating only when a new pivot pair forms.
2. **Confluence Example** – Marks levels where Fibonacci and S/R overlap. Labels display the calculated confluence weight, giving a quick visual of areas with higher probability of reaction.
3. **SR Logistic Regression** – Plots dynamic support/resistance zones that change color according to their status (active, validated, broken). Pivot markers appear when new zones are created.

## Commenting and Style

- Keep each example heavily commented so developers can follow the reasoning step by step.
- When integrating libraries, include brief comments explaining why a function or type is imported and how it affects the chart.
- Prefer small logical sections separated by headings (e.g. `// ── Inputs ──`, `// ── Calculation ──`) to make scripts easy to read and modify.

Following these guidelines ensures the example scripts remain clear references for future development.
