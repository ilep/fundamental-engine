# Methodology

## NOPAT

The default starting point is EBIT or operating income, adjusted for explicitly identified
exceptional operating items. Taxes must use an explicit policy: normalized rate, effective
reported rate, or cash taxes.

## Invested capital

The financing approach is:

```text
equity + interest-bearing debt + included finance leases - selected cash - excluded goodwill
```

The preferred period denominator is average beginning and ending invested capital. Users must
choose whether goodwill is included and whether all cash, only documented excess cash, or no
cash is deducted.

## ROIC

```text
NOPAT / average invested capital
```

The default method is not applicable to banks, insurers, and similar financial institutions.

## Owner earnings

```text
net income + D&A + non-cash SBC - required working capital
- exceptional items - maintenance capex
```

Maintenance capex is rarely observable. The engine therefore supports total capex, a D&A
proxy, an explicit analyst estimate, or a scenario range. SBC is added back as a non-cash
charge, but dilution must be reviewed separately.

## EPV

Strict EPV assumes no growth:

```text
normalized NOPAT / cost of capital
```

Non-operating assets and net debt are applied after enterprise value. Supplying a non-zero
growth rate is supported but is labelled as a growing perpetuity rather than strict EPV.

