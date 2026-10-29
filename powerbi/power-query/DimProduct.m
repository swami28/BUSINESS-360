let
    Sep = if Text.Contains(ProjectRoot, "\") then "\" else "/",
    Source = Csv.Document(File.Contents(ProjectRoot & Sep & "data" & Sep & "source" & Sep & "DimProduct.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"ProductKey", Int64.Type}, {"ProductName", type text}, {"Category", type text}}, "en-US"),
    Trimmed = Table.TransformColumns(Types, {{"ProductName", Text.Trim, type text}, {"Category", Text.Trim, type text}})
in
    Trimmed
