let
    Sep = if Text.Contains(ProjectRoot, "\") then "\" else "/",
    Source = Csv.Document(File.Contents(ProjectRoot & Sep & "data" & Sep & "source" & Sep & "DimDepartment.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"DepartmentKey", Int64.Type}, {"DepartmentName", type text}}, "en-US"),
    Trimmed = Table.TransformColumns(Types, {{"DepartmentName", Text.Trim, type text}})
in
    Trimmed
