# Data contract and source inventory

| Table | Demo source | Grain / unique key | Required columns |
|---|---|---|---|
| FactSales | SQLite, exported to CSV | order line / `(OrderID, LineNumber)` | OrderID, LineNumber, DateKey, ProductKey, RegionKey, DepartmentKey, Quantity, SalesAmount, CostAmount |
| DimDate | SQLite, exported to CSV | day / DateKey | DateKey (YYYYMMDD integer), Date (ISO date), Month, MonthNumber, Quarter, Year |
| DimProduct | CSV | product / ProductKey | ProductKey, ProductName, Category |
| DimRegion | CSV | region / RegionKey | RegionKey, City, State, Country |
| DimDepartment | CSV | department / DepartmentKey | DepartmentKey, DepartmentName |

All keys are required and must match; the sample rejects blanks and duplicate keys. SQL stores money as integer cents in `SalesCents` and `CostCents`; exported values are decimal currency units. Imported Power BI amount fields use fixed decimal currency. `OrderID` is text; keys and quantity are integers. `Date` is a true date in the model. Month names are English in the sample.

With the fixed seed, the demo contains 4,479 fact lines across 1,800 orders and 1,096 dates (2023-01-01 through 2025-12-31), with 165 negative lines. These are generated examples, not customer results. Run the build and validator rather than assuming these numbers for modified data.

For actual sources, record filename/DB/table, owner, refresh schedule, grain, key, row count, column types, date range, units/currency, and a trusted source control total before transformation. Replace the generator and adapt Power Query/SQL to the real schema. Review duplicates at the actual fact grain; repeated OrderIDs may be valid. Investigate missing or invalid values and unmatched keys and document exceptions; never silently remove negative transactions. Reconcile before and after cleaning, and configure source credentials/gateways securely in Power BI. The synthetic generator is not a production ETL pipeline.
