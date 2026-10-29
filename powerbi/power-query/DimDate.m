let
    Sep = if Text.Contains(ProjectRoot, "\") then "\" else "/",
    Source = Csv.Document(File.Contents(ProjectRoot & Sep & "data" & Sep & "generated" & Sep & "DimDate.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"DateKey", Int64.Type}, {"Date", type date}, {"Month", type text}, {"MonthNumber", Int64.Type}, {"Quarter", Int64.Type}, {"Year", Int64.Type}}, "en-US")
in
    Types
