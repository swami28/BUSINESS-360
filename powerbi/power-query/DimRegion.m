let
    Sep = if Text.Contains(ProjectRoot, "\") then "\" else "/",
    Source = Csv.Document(File.Contents(ProjectRoot & Sep & "data" & Sep & "source" & Sep & "DimRegion.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"RegionKey", Int64.Type}, {"City", type text}, {"State", type text}, {"Country", type text}}, "en-US"),
    Trimmed = Table.TransformColumns(Types, {{"City", Text.Trim, type text}, {"State", Text.Trim, type text}, {"Country", Text.Trim, type text}})
in
    Trimmed
