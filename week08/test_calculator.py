# -*- coding: utf-8 -*-
import unittest

from calculator import ParkingCalculator


class ParkingCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.calculator = ParkingCalculator()

    def calculate(self, entry, exit_):
        return self.calculator.calculate_parking(entry, exit_)

    def test_free_period(self):
        self.assertEqual(self.calculate("10:00", "10:20")["fee"], 0)

    def test_free_period_boundary(self):
        self.assertEqual(self.calculate("10:00", "10:30")["fee"], 0)

    def test_first_charge_unit(self):
        self.assertEqual(self.calculate("10:00", "10:40")["fee"], 500)

    def test_partial_unit_is_rounded_up(self):
        self.assertEqual(self.calculate("10:00", "10:41")["fee"], 1_000)

    def test_daily_maximum(self):
        self.assertEqual(self.calculate("10:00", "20:00")["fee"], 20_000)

    def test_crossing_midnight(self):
        record = self.calculate("23:00", "01:00")
        self.assertEqual(record["duration_minutes"], 120)
        self.assertEqual(record["fee"], 4_500)

    def test_hour_overflow_is_corrected(self):
        record = self.calculate("25:00", "02:30")
        self.assertEqual((record["entry"], record["exit"]), ("01:00", "02:30"))
        self.assertEqual(record["fee"], 3_000)

    def test_minute_overflow_is_corrected(self):
        record = self.calculate("09:65", "11:15")
        self.assertEqual(record["entry"], "10:05")
        self.assertEqual(record["duration_minutes"], 70)
        self.assertEqual(record["fee"], 2_000)

    def test_same_time_means_next_day(self):
        record = self.calculate("10:00", "10:00")
        self.assertEqual(record["duration_minutes"], 1_440)
        self.assertEqual(record["fee"], 20_000)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            self.calculate("abc", "10:00")
        self.assertEqual(self.calculator.get_all_records(), [])

    def test_remove_record_recalculates_total(self):
        self.calculate("10:00", "10:40")
        self.calculate("10:00", "10:41")
        self.calculator.remove_record(0)
        self.assertEqual(len(self.calculator.get_all_records()), 1)
        self.assertEqual(self.calculator.get_total_sum(), 1_000)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ParkingCalculatorTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)

    print("\n" + "=" * 34)
    print("테스트 결과 요약")
    print(f"통과 (Pass): {passed}")
    print(f"실패 (Fail): {len(result.failures)}")
    print(f"에러 (Error): {len(result.errors)}")
    print("=" * 34)

    raise SystemExit(0 if result.wasSuccessful() else 1)
