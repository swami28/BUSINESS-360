#!/usr/bin/env python3
"""Rebuild the synthetic SQLite source and Power BI-ready SQL extracts."""
import calendar
import csv
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data' / 'source'
OUT = ROOT / 'data' / 'generated'


def read_dimension(name):
    with (SOURCE / f'{name}.csv').open(newline='', encoding='utf-8') as f:
        return list(csv.reader(f))


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    db = OUT / 'business360.sqlite'
    db.unlink(missing_ok=True)
    conn = sqlite3.connect(db)
    try:
        conn.executescript((ROOT / 'sql' / 'schema.sql').read_text(encoding='utf-8'))
        for name in ('DimDepartment', 'DimProduct', 'DimRegion'):
            rows = read_dimension(name)
            placeholders = ','.join('?' for _ in rows[0])
            conn.executemany(f'INSERT INTO {name} VALUES ({placeholders})', rows[1:])
        start, end = date(2023, 1, 1), date(2025, 12, 31)
        dates = []
        day = start
        while day <= end:
            dates.append((int(day.strftime('%Y%m%d')), day.isoformat(), calendar.month_name[day.month], day.month, (day.month - 1) // 3 + 1, day.year))
            day += timedelta(days=1)
        conn.executemany('INSERT INTO DimDate VALUES (?,?,?,?,?,?)', dates)
        rng = random.Random(360)
        # Base prices and costs are integer cents; synthetic, not real results.
        prices = [(85000, 62000), (24000, 15500), (18000, 12500), (35000, 25000), (16000, 10500), (1400, 800), (4200, 2600), (900, 500)]
        lines = []
        for order in range(1, 1801):
            order_day = start + timedelta(days=rng.randrange((end - start).days + 1))
            region, department = rng.randint(1, 5), rng.randint(1, 4)
            for line in range(1, rng.randint(1, 4) + 1):
                product = rng.randint(1, len(prices))
                qty = rng.randint(1, 5)
                # Negative lines are independent adjustments, not matched returns.
                if rng.random() < 0.035:
                    qty = -qty
                price, cost = prices[product - 1]
                lines.append((f'ORD-{order:05d}', line, int(order_day.strftime('%Y%m%d')), product, region, department, qty, qty * price, qty * cost))
        conn.executemany('INSERT INTO FactSales VALUES (?,?,?,?,?,?,?,?,?)', lines)
        conn.commit()
        exports = {
            'DimDate': 'SELECT DateKey, Date, Month, MonthNumber, Quarter, Year FROM DimDate ORDER BY DateKey',
            # Decimal strings avoid a binary floating-point conversion in the extract.
            'FactSales': '''SELECT OrderID, LineNumber, DateKey, ProductKey, RegionKey, DepartmentKey,
                Quantity, printf('%.2f', SalesCents / 100.0) AS SalesAmount,
                printf('%.2f', CostCents / 100.0) AS CostAmount
                FROM FactSales ORDER BY OrderID, LineNumber''',
        }
        for name, query in exports.items():
            cursor = conn.execute(query)
            with (OUT / f'{name}.csv').open('w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([column[0] for column in cursor.description])
                writer.writerows(cursor)
        print(f'Created {db.relative_to(ROOT)}: {len(lines)} lines, 1800 orders, {len(dates)} dates.')
        print('Exported DimDate.csv and FactSales.csv from SQLite.')
    finally:
        conn.close()


if __name__ == '__main__':
    build()
