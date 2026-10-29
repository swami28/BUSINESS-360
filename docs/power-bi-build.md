# Build the Power BI report

These steps describe work to perform in Power BI Desktop; this repository does not contain a completed PBIX. Build and validate the sample first using the README. In Power BI, **Get Data → Blank Query → Advanced Editor** and create the parameter and five queries as described in [Power Query setup](../powerbi/power-query/README.md). Close & Apply.

## Model

In Model view create these active, single-direction, one-to-many relationships (dimension filters fact):

| One side | Many side |
|---|---|
| DimDate[DateKey] | FactSales[DateKey] |
| DimProduct[ProductKey] | FactSales[ProductKey] |
| DimRegion[RegionKey] | FactSales[RegionKey] |
| DimDepartment[DepartmentKey] | FactSales[DepartmentKey] |

Mark `DimDate` as the date table using `DimDate[Date]`; ensure it is unique, continuous, and has date type. Sort `DimDate[Month]` by `DimDate[MonthNumber]`. Create a column `Year Month = FORMAT('DimDate'[Date], "yyyy-MM")` for an unambiguous chronological monthly axis. Hide foreign keys and line number from report view if desired, but keep them available for validation. Disable implicit summarization on keys. Do not join dimensions to one another.

## Measures

Add the definitions in [measures.dax](../powerbi/measures.dax), one at a time, via **New measure**. Format sales, cost, profit and AOV as USD with two decimals; margin and growth as percentages; units and orders as whole numbers. Blank denominators return blank, not zero. AOV is calculated in the current filter context; distinct order counts are not generally additive across product groups because one order can contain multiple products.

`SAMEPERIODLASTYEAR` requires the marked continuous date table. For YoY, compare equivalent date ranges. A year-to-date selection should be compared with the same dates in the previous year; a full prior year is not comparable to a partial current year. Validate leap-day and partial-month behavior in the actual model. The earliest year has no prior year in the demo and should show blank rather than a fabricated growth figure.

## Pages and interactions

1. **Executive Overview** — cards: Total Sales, Total Profit, Profit Margin %, Total Orders; line chart: `DimDate[Year Month]` against Total Sales; bar chart: DepartmentName against Total Sales; region bar chart: Country against Total Sales. Add date, department, product category and country slicers.
2. **Department Performance** — bar chart: DepartmentName against Total Sales and Total Profit; table: DepartmentName, Total Sales, Total Cost, Total Profit, Profit Margin %, Units Sold, Total Orders. Add the same relevant slicers. Sort by sales or profit and investigate high sales/low margin.
3. **Trend Analysis** — line chart: Year Month against Total Sales and Sales Previous Year; table: Year Month, Total Sales, Sales Previous Year, Sales YoY Growth %, Profit Margin %. Add date and department slicers; use actual date slicer for comparable ranges.
4. **Detailed Analysis** — table: OrderID, LineNumber, Date, DepartmentName, ProductName, City, Quantity, SalesAmount, CostAmount. Add DepartmentName to the drill-through filter well, enable **Keep all filters**, and add a back button. From a department visual, right-click a department and drill through. Also add product and region slicers as appropriate.

Use consistent titles and labels, and test cross-filtering and drill-through. On the detail table, set numeric fact columns to **Don't summarize**. If you add slicers to multiple pages, use View → Sync slicers if shared filtering is desired. A region bar chart avoids map-geocoding ambiguity. Save the PBIX locally (ignored by Git by default). See [validation.md](validation.md) before sharing the report.
