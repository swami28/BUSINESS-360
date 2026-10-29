# Business 360 — Sales Analytics

A reproducible sales analytics starter project using **CSV, SQLite, Power Query, Power BI, DAX and DAX Studio**. It models order lines in a star schema and supplies SQL, data checks, Power Query imports, measures, and a four-page Power BI build specification.

> **Status and scope:** All included data is synthetic and generated locally. The SQL database, extracts and checks are runnable; the Power BI report must be assembled in Power BI Desktop using the supplied files. No `.pbix` is included, and DAX, report visuals and DAX Studio timings have not been tested in Power BI in this environment. Do not describe the demo numbers as actual business results or claim measured performance improvements.

## Quick start

Prerequisite: Python 3.9+ (standard library only). Power BI Desktop is needed to build the report; DAX Studio is optional for profiling.

```sh
python scripts/build_demo.py
python scripts/validate.py
python scripts/report.py
python -m unittest discover -s tests -v
```

The build recreates `data/generated/business360.sqlite` and exports `FactSales.csv` and `DimDate.csv` from that database. The product, department and region dimension CSVs in `data/source/` act as the spreadsheet sources. Generated files are ignored by Git: run the build after cloning. **Rebuilding overwrites the generated database and extracts**; keep any real data elsewhere.

For Power BI Desktop, follow [the step-by-step report build](docs/power-bi-build.md) and [Power Query setup](powerbi/power-query/README.md). SQL is in [sql/analysis.sql](sql/analysis.sql), and DAX is in [powerbi/measures.dax](powerbi/measures.dax).

## Architecture

```text
CSV dimensions ──────────────────────────────┐
                                             ├─> Power Query ─> star model ─> DAX ─> report
SQLite FactSales + DimDate ─> CSV extracts ──┘                               └─> DAX Studio checks
```

The default Power BI workflow imports SQL **extracts**, not a direct database connection; an optional SQLite ODBC example is provided. SQLite also contains copies of the dimensions for SQL joins and reconciliation. This sample uses SQLite, not SQL Server. Replace the adapter and data contracts if your actual SQL source differs.

## Business questions & metric definitions

- Which departments and regions contribute most sales and profit?
- How do sales change by month and compared with the same period last year?
- Where is sales growth accompanied by weaker profit margin?
- Which products and transactions explain a department or region's results?

The synthetic demo has one reporting currency (labeled USD for display, without currency conversion). **Sales** is the signed `SalesAmount` after negative adjustments, **cost** is signed `CostAmount`, and **profit** is sales minus cost. Margin is profit / sales; units are signed quantity; orders are distinct `OrderID` values; average order value is sales / distinct orders. Negative lines are synthetic independent adjustments, not linked to original orders; therefore order count includes orders with negative lines and should not be interpreted as net orders. In real data, confirm returns, discounts, tax, order status and currency treatment with stakeholders before reusing these definitions.

The fact grain is **one order line**, uniquely identified by `(OrderID, LineNumber)`. Each order shares its date, region and department across its lines; products can differ. Date covers every day in 2023–2025. No targets are modeled. Add targets only when available, in a separate table at a documented period/department grain; never join them to transaction rows and sum duplicated amounts.

## Data quality and limitations

The generator uses a fixed seed. `validate.py` checks uniqueness, blanks, consecutive dates, unmatched keys, SQL foreign keys and SQL/CSV totals overall and by month, department, region and product, using integer cents. It retains negative adjustments. Duplicate order IDs are expected across lines; duplicate `(OrderID, LineNumber)` pairs are not. In real data, investigate missing keys, invalid dates, negative amounts and duplicate lines instead of silently dropping them; document any quarantine or correction. The script validates the source and extracts—not the Power BI model or visual results. See [validation and profiling](docs/validation.md) for manual report checks and a DAX Studio procedure.

## Repository guide

| Path | Contents |
|---|---|
| `data/source/` | Synthetic CSV dimensions |
| `scripts/build_demo.py` | Deterministic SQL database and extract builder |
| `scripts/validate.py`, `tests/` | Reconciliation checks and regression tests |
| `sql/` | SQLite schema and business queries |
| `powerbi/` | Power Query imports, optional ODBC example and DAX measures |
| `docs/` | Report assembly, validation and profiling instructions |

Real data requires its own source inventory, key/grain mapping, security and refresh configuration. See [data contract](docs/data-contract.md) before substituting it.
