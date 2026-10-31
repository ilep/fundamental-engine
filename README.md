# Fundamental Engine

`fundamental-engine` is a deterministic calculation library for fundamental investment
analysis. Agents and data providers may prepare inputs, but every financial calculation is
performed by explicit, testable Python code.

The first release implements:

- normalized financial-period models with field-level provenance;
- NOPAT and invested-capital policies;
- ROIC and incremental ROIC;
- CFO-based FCF and FCFF;
- owner earnings with maintenance-capex scenarios;
- EPV, earnings-multiple valuation, DCF, and margin of safety;
- bear/base/bull scenarios;
- adapters for `ai-fund` normalized JSON and EOD-shaped fundamentals.

## Install for development

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

## Design rules

1. The core package never imports an LLM, browser, database, or messaging client.
2. Missing data stays missing; adapters never turn absent values into economic zeroes.
3. Every result reports its formula, inputs, assumptions, warnings, and confidence.
4. Accounting choices are explicit policies, not hidden implementation details.
5. Financial institutions require a separate methodology and are rejected by default.

See `docs/methodology.md` for definitions and `examples/basic_analysis.py` for usage.

