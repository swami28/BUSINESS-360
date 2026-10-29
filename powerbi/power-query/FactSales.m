let
    Sep = if Text.Contains(ProjectRoot, "\") then "\" else "/",
    Source = Csv.Document(File.Contents(ProjectRoot & Sep & "data" & Sep & "generated" & Sep & "FactSales.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"OrderID", type text}, {"LineNumber", Int64.Type}, {"DateKey", Int64.Type}, {"ProductKey", Int64.Type}, {"RegionKey", Int64.Type}, {"DepartmentKey", Int64.Type}, {"Quantity", Int64.Type}, {"SalesAmount", Currency.Type}, {"CostAmount", Currency.Type}}, "en-US")
in
    Types
