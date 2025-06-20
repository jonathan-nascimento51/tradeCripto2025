# Library Guidelines

All helper libraries must keep a compact and reusable structure.

- Declare the file as a Pine library using `library("<Name>", true)` so it can be imported by other scripts.
- Keep implementation around **300 lines** or less to maintain readability.
- Export all functions and user defined types that should be consumed externally.
- Each library must have a **matching test script** under `tests/` demonstrating its usage.
- Reuse the colors and styles defined in `style_lib.pine` for visual consistency across all indicators.

These conventions help maintain an organized code base and make individual components easier to validate and extend.
