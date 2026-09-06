# 1-Year Share-Price Performance Comparison

**Period:** 2025-09-04 to 2026-09-04 (the one-year range returned by Yahoo Finance's price-series tool)

**Method:** For each security with usable data, performance is calculated from the earliest and latest returned closing prices:

`(latest close / earliest close - 1) × 100`

| Company | Ticker | Data range | Earliest returned close | Latest returned close | Price performance |
|---|---|---|---:|---:|---:|
| Legal & General | [LGEN.L](https://finance.yahoo.com/quote/LGEN.L/) | 2025-09-04 to 2026-09-04; 254 trading days | 235.0135 (2025-09-04) | 295.7000 (2026-09-04) | **+25.82%** |
| Aviva | [AV.L](https://finance.yahoo.com/quote/AV.L/) | 2025-09-04 to 2026-09-04; 254 trading days | 645.4055 (2025-09-04) | 729.8000 (2026-09-04) | **+13.08%** |
| AIICO Insurance | [AIICO.LG](https://finance.yahoo.com/quote/AIICO.LG/) | — | — | — | **Failed — Yahoo Finance returned no data** |
| MTN Group | [MTN.JO](https://finance.yahoo.com/quote/MTN.JO/) | 2025-09-04 to 2026-09-04; 251 trading days | 13,865.4443 (2025-09-04) | 19,931.0000 (2026-09-04) | **+43.75%** |

## Notes and caveats

- The figures are **closing-price changes**, not dividend-adjusted total returns. The tool output did not separately identify the values as adjusted closes.
- AIICO Insurance's lookup failed explicitly, so no performance estimate is provided; no number has been guessed.
- Percentage changes are comparable within each security. Absolute prices use the respective exchange currencies and quoting units and should not be compared directly.
- The arithmetic was independently reviewed: LGEN.L = +25.82%, AV.L = +13.08%, and MTN.JO = +43.75% when rounded to two decimal places.
