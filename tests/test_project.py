import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_demo
import validate


class ProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_demo.build()

    def test_validation_passes(self):
        validate.validate()

    def test_validation_detects_unmatched_key(self):
        original = validate.rows
        def altered(path):
            data = original(path)
            if path.name == 'FactSales.csv':
                data[0]['RegionKey'] = '999999'
            return data
        with patch.object(validate, 'rows', side_effect=altered):
            with self.assertRaisesRegex(ValueError, 'Unmatched RegionKey'):
                validate.validate()

    def test_validation_detects_reconciliation_error(self):
        original = validate.rows
        def altered(path):
            data = original(path)
            if path.name == 'FactSales.csv':
                data[0]['SalesAmount'] = '123456789.00'
            return data
        with patch.object(validate, 'rows', side_effect=altered):
            with self.assertRaisesRegex(ValueError, 'reconciliation failed'):
                validate.validate()

    def test_repeat_build_is_deterministic(self):
        path = ROOT / 'data/generated/FactSales.csv'
        before = path.read_bytes()
        build_demo.build()
        self.assertEqual(before, path.read_bytes())


if __name__ == '__main__':
    unittest.main()
