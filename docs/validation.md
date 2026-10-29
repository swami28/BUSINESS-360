# Validation and performance checklist

## Automated source checks

Run `python scripts/validate.py` after every demo rebuild. It compares the SQL source and the CSV model inputs (including dimensions and sliced totals), checks foreign keys, blanks, duplicate keys/lines and date continuity. Run `python -m unittest discover -s tests -v` for regression checks, including deliberate key and amount corruption. These checks do **not** execute Power Query, DAX or Power BI visuals.

## Power BI reconciliation (manual)

1. Refresh all queries; review load errors and row counts. For the unchanged demo, expect 4,479 fact lines, 1,800 distinct orders, 1,096 date rows, 8 products, 5 regions and 4 departments. If the generator or input dimensions change, recompute instead of relying on these reference counts.
2. With all filters cleared, compare cards and table against `python scripts/report.py` (the last query) or run `sql/analysis.sql` against `data/generated/business360.sqlite`. For the unchanged demo: sales 2,860,736.00, cost 2,007,025.00, profit 853,711.00, units 12,486. Confirm the margin and AOV are profit/sales and sales/distinct orders respectively.
3. Compare department and monthly visual totals to the corresponding SQL queries. Match the date range and filter context, including negative adjustments. Slice by product and region and cross-check with SQL; sums of distinct orders across products may exceed the overall order count.
4. Check date table and relationship directions; inspect unmatched-key/blank members, duplicates and negative lines. Drill through from a department and confirm details match the selected context and totals. Test each slicer and interactions.
5. Test YoY on a complete year, a single month and an equivalent partial period, including the first year with no prior data. Check leap-day behavior and absence of division-by-zero errors. Record exclusions and differences rather than silently correcting totals.
6. If a target table is later added, document its grain, test slicers and avoid duplicating target values across fact rows. No target is included in this sample.

## DAX Studio profiling (manual)

1. In Power BI Desktop, open **View → Performance Analyzer**, start recording, refresh the suspect visual, and copy its DAX query. Note the page, slicers, data refresh state and visual.
2. Connect DAX Studio to the open Power BI model and run the copied query. Record elapsed/server timings and query plan when supported and enabled. Repeat the same scenario and note warm/cold cache conditions, tool version and number of runs.
3. Investigate model relationships, high-cardinality columns, visual row counts and expensive measures. Make one change at a time; rerun under the same conditions, record before/after results and verify numeric equivalence.
4. Report timing improvements only if measured; no benchmark or performance improvement is claimed for this starter project.

## Demo / interview narrative

Explain the business question, source grain and signed sales definitions, then show a department or month comparison and drill through to its details. A trend is a prompt for investigation, not proof of causation. Distinguish the supplied synthetic starter from any real implementation; describe only work you actually performed and can demonstrate.
