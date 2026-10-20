# -*- coding: utf-8 -*-
import math
import re


class ParkingCalculator:
    # ========================================
    # Parking Fee Setting Values
    # ========================================
    FREE_MINUTES = 30       # First 30 minute is free
    RATE_MINUTES = 10       # Charge unit is 10 minutes
    RATE_AMOUNT = 500       # 500 won for each unit
    MAX_FEE = 20000         # Maximum fee for one parking record
    MINUTES_PER_DAY = 24 * 60

    def __init__(self):
        # List for save all parking records
        self.records = []

    # ========================================
    # 1. Time Parse and Auto Correction
    # ========================================
    @staticmethod
    def parse_and_correct_time(time_text):
        """Input HH:MM string and convert to total minutes."""

        # Check input data type
        if not isinstance(time_text, str):
            raise ValueError("시간은 HH:MM 형식으로 입력해주세요.")

        # Use regular expression for checking time format
        time_match = re.fullmatch(r"\s*(\d+)\s*:\s*(\d+)\s*", time_text)

        if time_match is None:
            raise ValueError("시간은 HH:MM 형식으로 입력해주세요.")

        # Convert hour and minute into integer
        hour_value = int(time_match.group(1))
        minute_value = int(time_match.group(2))

        # Calculate total minutes
        total_minutes = (hour_value * 60) + minute_value

        # Auto correct time into one day range
        corrected_minutes = total_minutes % ParkingCalculator.MINUTES_PER_DAY

        return corrected_minutes

    # ========================================
    # 2. Time Formatting Function
    # ========================================
    @staticmethod
    def format_time(total_minutes):
        # Correct total minutes first
        corrected_value = total_minutes % ParkingCalculator.MINUTES_PER_DAY

        # Separate Hour and Minute
        hour = corrected_value // 60
        minute = corrected_value % 60

        # Return HH:MM Format
        return f"{hour:02d}:{minute:02d}"

    # ========================================
    # 3. Parking Fee Calculation
    # ========================================
    def calculate_parking(self, entry_text, exit_text):
        """Calculate parking duration and fee, and save record."""

        # Parse Entry and Exit Time
        entry_minutes = self.parse_and_correct_time(entry_text)
        exit_minutes = self.parse_and_correct_time(exit_text)

        # Calculate Parking Duration
        parking_minutes = exit_minutes - entry_minutes

        # If Exit Time is next day
        if parking_minutes <= 0:
            parking_minutes = parking_minutes + self.MINUTES_PER_DAY

        # Calculate Parking Fee
        if parking_minutes <= self.FREE_MINUTES:
            parking_fee = 0
        else:
            # Remove Free Minutes
            charged_minutes = parking_minutes - self.FREE_MINUTES

            # Round Up Charging Unit
            charge_count = math.ceil(charged_minutes / self.RATE_MINUTES)

            # Calculate Basic Fee
            calculated_fee = charge_count * self.RATE_AMOUNT

            # Apply Maximum Fee
            parking_fee = min(calculated_fee, self.MAX_FEE)

        # Make duration text
        parking_hour = parking_minutes // 60
        parking_minute = parking_minutes % 60
        duration_text = f"{parking_hour}시간 {parking_minute}분"

        # Make one parking record
        parking_record = {
            "entry": self.format_time(entry_minutes),
            "exit": self.format_time(exit_minutes),
            "duration_minutes": parking_minutes,
            "duration": duration_text,
            "fee": parking_fee,
        }

        # Save and return record
        self.records.append(parking_record)
        return parking_record.copy()

    # ========================================
    # 4. Parking Record Management
    # ========================================
    def get_all_records(self):
        """Return copied parking record list."""
        return [record.copy() for record in self.records]

    def remove_record(self, record_index):
        """Remove one parking record by index."""
        if not isinstance(record_index, int):
            raise IndexError("삭제할 주차 기록이 없습니다.")

        if record_index < 0 or record_index >= len(self.records):
            raise IndexError("삭제할 주차 기록이 없습니다.")

        return self.records.pop(record_index)

    def get_total_sum(self):
        """Return total fee of all parking records."""
        total_fee = 0

        for record in self.records:
            total_fee = total_fee + record["fee"]

        return total_fee
