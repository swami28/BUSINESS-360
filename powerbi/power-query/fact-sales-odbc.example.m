// Optional: requires a working 64-bit SQLite ODBC DSN configured separately.
// Replace the FactSales query with this; do not create a second FactSales table.
let
    Source = Odbc.Query("dsn=Business360SQLite", "SELECT OrderID, LineNumber, DateKey, ProductKey, RegionKey, DepartmentKey, Quantity, SalesCents / 100.0 AS SalesAmount, CostCents / 100.0 AS CostAmount FROM FactSales"),
    Types = Table.TransformColumnTypes(Source, {{"OrderID", type text}, {"LineNumber", Int64.Type}, {"DateKey", Int64.Type}, {"ProductKey", Int64.Type}, {"RegionKey", Int64.Type}, {"DepartmentKey", Int64.Type}, {"Quantity", Int64.Type}, {"SalesAmount", Currency.Type}, {"CostAmount", Currency.Type}}, "en-US")
in
    Types
