#!/usr/bin/env python3
"""Run the supplied SQLite analysis queries without requiring the sqlite3 CLI."""
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'generated' / 'business360.sqlite'
if not DB.exists():
    sys.exit('Database missing. Run python scripts/build_demo.py first.')
# Strip line comments before splitting; the supplied SQL has no quoted semicolons.
sql = (ROOT / 'sql' / 'analysis.sql').read_text(encoding='utf-8')
sql = '\n'.join(line.split('--', 1)[0] for line in sql.splitlines())
queries = sql.split(';')
with sqlite3.connect(f'file:{DB}?mode=ro', uri=True) as conn:
    for query in queries:
        if not any(line.strip() and not line.lstrip().startswith('--') for line in query.splitlines()):
            continue
        cur = conn.execute(query)
        print('\n' + ' | '.join(col[0] for col in cur.description))
        for row in cur:
            print(' | '.join(str(value) for value in row))
