-- SQLite demo schema. Money is stored as integer cents to avoid floating-point
-- rounding during source reconciliation. One fact row is one order line.
PRAGMA foreign_keys = ON;
CREATE TABLE DimDate (
    DateKey INTEGER PRIMARY KEY,
    Date TEXT NOT NULL UNIQUE,
    Month TEXT NOT NULL,
    MonthNumber INTEGER NOT NULL CHECK (MonthNumber BETWEEN 1 AND 12),
    Quarter INTEGER NOT NULL CHECK (Quarter BETWEEN 1 AND 4),
    Year INTEGER NOT NULL
);
CREATE TABLE DimProduct (ProductKey INTEGER PRIMARY KEY, ProductName TEXT NOT NULL, Category TEXT NOT NULL);
CREATE TABLE DimRegion (RegionKey INTEGER PRIMARY KEY, City TEXT NOT NULL, State TEXT NOT NULL, Country TEXT NOT NULL);
CREATE TABLE DimDepartment (DepartmentKey INTEGER PRIMARY KEY, DepartmentName TEXT NOT NULL UNIQUE);
CREATE TABLE FactSales (
    OrderID TEXT NOT NULL,
    LineNumber INTEGER NOT NULL,
    DateKey INTEGER NOT NULL REFERENCES DimDate(DateKey),
    ProductKey INTEGER NOT NULL REFERENCES DimProduct(ProductKey),
    RegionKey INTEGER NOT NULL REFERENCES DimRegion(RegionKey),
    DepartmentKey INTEGER NOT NULL REFERENCES DimDepartment(DepartmentKey),
    Quantity INTEGER NOT NULL,
    SalesCents INTEGER NOT NULL,
    CostCents INTEGER NOT NULL,
    PRIMARY KEY (OrderID, LineNumber)
);
CREATE INDEX idx_sales_date ON FactSales(DateKey);
CREATE INDEX idx_sales_department ON FactSales(DepartmentKey);
