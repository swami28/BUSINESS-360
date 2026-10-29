#!/usr/bin/env python3
"""Fail on data/model problems and reconcile the SQL database with CSV inputs."""
import csv
import sqlite3
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def cents(value):
    amount = Decimal(value) * 100
    require(amount == amount.to_integral_value(), f'Fractional cent: {value}')
    return int(amount)


def validate():
    generated = ROOT / 'data' / 'generated'
    db = generated / 'business360.sqlite'
    require(db.exists(), 'Database missing. Run python scripts/build_demo.py first.')
    dimensions = {}
    for name, key, folder in [('DimDate', 'DateKey', generated), ('DimProduct', 'ProductKey', ROOT / 'data/source'), ('DimRegion', 'RegionKey', ROOT / 'data/source'), ('DimDepartment', 'DepartmentKey', ROOT / 'data/source')]:
        data = rows(folder / f'{name}.csv')
        require(data, f'{name} is empty')
        keys = [r[key] for r in data]
        require(all(keys) and len(keys) == len(set(keys)), f'{name} keys are blank or duplicated')
        require(all(all(value is not None and value.strip() for value in row.values()) for row in data), f'{name} has blanks')
        dimensions[name] = {r[key]: r for r in data}
    dates = sorted(date.fromisoformat(r['Date']) for r in dimensions['DimDate'].values())
    require(len(set(dates)) == len(dates), 'Duplicate dates')
    require(len(dates) == (dates[-1] - dates[0]).days + 1, 'Date table has gaps')
    for r in dimensions['DimDate'].values():
        d = date.fromisoformat(r['Date'])
        require(r['DateKey'] == d.strftime('%Y%m%d') and int(r['Year']) == d.year and int(r['MonthNumber']) == d.month and int(r['Quarter']) == (d.month - 1) // 3 + 1, 'Date attributes inconsistent')
    facts = rows(generated / 'FactSales.csv')
    require(facts, 'FactSales is empty')
    seen = set()
    grouped = defaultdict(lambda: [0, 0, 0])
    orders = set()
    negatives = 0
    for r in facts:
        require(all(value is not None and value.strip() for value in r.values()), 'Fact row has blanks')
        line = (r['OrderID'], r['LineNumber'])
        require(line not in seen, f'Duplicate order line: {line}')
        seen.add(line)
        orders.add(r['OrderID'])
        for dim, key in [('DimDate', 'DateKey'), ('DimProduct', 'ProductKey'), ('DimRegion', 'RegionKey'), ('DimDepartment', 'DepartmentKey')]:
            require(r[key] in dimensions[dim], f'Unmatched {key}: {r[key]}')
        q, sales, cost = int(r['Quantity']), cents(r['SalesAmount']), cents(r['CostAmount'])
        negatives += q < 0
        # Validate both totals and date/department/region/product slices in cents.
        for group in [('all', ''), ('month', r['DateKey'][:6]), ('department', r['DepartmentKey']), ('region', r['RegionKey']), ('product', r['ProductKey'])]:
            grouped[group][0] += q
            grouped[group][1] += sales
            grouped[group][2] += cost
    with sqlite3.connect(db) as conn:
        require(not conn.execute('PRAGMA foreign_key_check').fetchall(), 'Database foreign-key violations')
        require(conn.execute('SELECT COUNT(*) FROM FactSales').fetchone()[0] == len(facts), 'Fact row count differs from database')
        require(conn.execute('SELECT COUNT(DISTINCT OrderID) FROM FactSales').fetchone()[0] == len(orders), 'Distinct order count differs')
        queries = {
            'all': "SELECT '', SUM(Quantity), SUM(SalesCents), SUM(CostCents) FROM FactSales",
            'month': "SELECT substr(CAST(DateKey AS TEXT), 1, 6), SUM(Quantity), SUM(SalesCents), SUM(CostCents) FROM FactSales GROUP BY 1",
            'department': 'SELECT CAST(DepartmentKey AS TEXT), SUM(Quantity), SUM(SalesCents), SUM(CostCents) FROM FactSales GROUP BY 1',
            'region': 'SELECT CAST(RegionKey AS TEXT), SUM(Quantity), SUM(SalesCents), SUM(CostCents) FROM FactSales GROUP BY 1',
            'product': 'SELECT CAST(ProductKey AS TEXT), SUM(Quantity), SUM(SalesCents), SUM(CostCents) FROM FactSales GROUP BY 1',
        }
        for label, query in queries.items():
            actual = {str(k): [q, s, c] for k, q, s, c in conn.execute(query)}
            expected = {key: values for (kind, key), values in grouped.items() if kind == label}
            require(actual == expected, f'SQL/CSV reconciliation failed for {label}')
        for name, key in [('DimDate', 'DateKey'), ('DimDepartment', 'DepartmentKey'), ('DimProduct', 'ProductKey'), ('DimRegion', 'RegionKey')]:
            columns = [r[1] for r in conn.execute(f'PRAGMA table_info({name})')]
            db_rows = {str(row[0]): tuple(str(v) for v in row) for row in conn.execute(f'SELECT * FROM {name}')}
            csv_rows = {k: tuple(r[col] for col in columns) for k, r in dimensions[name].items()}
            require(db_rows == csv_rows, f'{name} CSV does not match database')
    q, sales, cost = grouped[('all', '')]
    print(f'PASS: {len(facts)} lines, {len(orders)} distinct orders, {negatives} negative adjustment lines, {len(dates)} consecutive dates.')
    print(f'SQL/CSV reconciled overall and by month, department, region and product: units={q}, sales={sales / 100:,.2f}, cost={cost / 100:,.2f}, profit={(sales-cost) / 100:,.2f}.')
    print('Power BI visuals, DAX and performance still require manual validation in Power BI Desktop.')


if __name__ == '__main__':
    try:
        validate()
    except (ValueError, OSError, sqlite3.Error, KeyError) as e:
        print(f'FAIL: {e}', file=sys.stderr)
        sys.exit(1)
