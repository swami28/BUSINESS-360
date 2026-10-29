-- SQLite; amounts in the database are integer cents. These queries include
-- negative adjustments. Divide by 100 for reporting currency units.

-- Sales by department
SELECT d.DepartmentName, SUM(f.SalesCents) / 100.0 AS TotalSales
FROM FactSales AS f JOIN DimDepartment AS d ON f.DepartmentKey = d.DepartmentKey
GROUP BY d.DepartmentKey, d.DepartmentName ORDER BY TotalSales DESC;

-- Monthly sales
SELECT dt.Year, dt.MonthNumber, dt.Month, SUM(f.SalesCents) / 100.0 AS TotalSales
FROM FactSales AS f JOIN DimDate AS dt ON f.DateKey = dt.DateKey
GROUP BY dt.Year, dt.MonthNumber, dt.Month ORDER BY dt.Year, dt.MonthNumber;

-- Profit by department
SELECT d.DepartmentName, SUM(f.SalesCents) / 100.0 AS TotalSales,
       SUM(f.CostCents) / 100.0 AS TotalCost,
       SUM(f.SalesCents - f.CostCents) / 100.0 AS Profit
FROM FactSales AS f JOIN DimDepartment AS d ON f.DepartmentKey = d.DepartmentKey
GROUP BY d.DepartmentKey, d.DepartmentName ORDER BY Profit DESC;

-- Grand totals and distinct order count for comparison with unfiltered Power BI.
SELECT COUNT(*) AS Lines, COUNT(DISTINCT OrderID) AS Orders,
       SUM(Quantity) AS UnitsSold, SUM(SalesCents) / 100.0 AS TotalSales,
       SUM(CostCents) / 100.0 AS TotalCost,
       SUM(SalesCents - CostCents) / 100.0 AS TotalProfit
FROM FactSales;
