# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from calculator import ParkingCalculator


class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("주차 요금 계산기")
        self.root.geometry("720x560")
        self.root.minsize(650, 480)

        # Parking calculator object
        self.calculator = ParkingCalculator()

        # Input mode value
        self.input_mode = tk.StringVar(value="manual")

        # Make all screen widgets
        self.make_mode_area()
        self.make_input_area()
        self.make_record_area()
        self.make_total_area()

        # Show first screen state
        self.change_input_mode()
        self.update_record_list()

    # ========================================
    # 1. Input Mode Area
    # ========================================
    def make_mode_area(self):
        mode_frame = ttk.LabelFrame(self.root, text="입력 방식", padding=10)
        mode_frame.pack(fill="x", padx=12, pady=(12, 6))

        manual_radio = ttk.Radiobutton(
            mode_frame,
            text="직접 입력",
            variable=self.input_mode,
            value="manual",
            command=self.change_input_mode,
        )
        manual_radio.pack(side="left", padx=(5, 20))

        dropdown_radio = ttk.Radiobutton(
            mode_frame,
            text="드롭다운 선택",
            variable=self.input_mode,
            value="dropdown",
            command=self.change_input_mode,
        )
        dropdown_radio.pack(side="left")

    # ========================================
    # 2. Time Input Area
    # ========================================
    def make_input_area(self):
        input_frame = ttk.LabelFrame(self.root, text="입차 및 출차 시각", padding=10)
        input_frame.pack(fill="x", padx=12, pady=6)

        # Manual input widgets
        self.manual_frame = ttk.Frame(input_frame)

        ttk.Label(self.manual_frame, text="입차").grid(row=0, column=0, padx=5)
        self.entry_time = ttk.Entry(self.manual_frame, width=10)
        self.entry_time.grid(row=0, column=1, padx=(0, 25))

        ttk.Label(self.manual_frame, text="출차").grid(row=0, column=2, padx=5)
        self.exit_time = ttk.Entry(self.manual_frame, width=10)
        self.exit_time.grid(row=0, column=3, padx=5)

        self.entry_time.insert(0, "09:00")
        self.exit_time.insert(0, "10:00")

        self.entry_time.bind(
            "<KeyRelease>",
            lambda event: self.auto_input_colon(self.entry_time),
        )
        self.exit_time.bind(
            "<KeyRelease>",
            lambda event: self.auto_input_colon(self.exit_time),
        )

        # Dropdown input widgets
        self.dropdown_frame = ttk.Frame(input_frame)

        hour_values = [f"{hour:02d}" for hour in range(24)]
        minute_values = [f"{minute:02d}" for minute in range(60)]

        ttk.Label(self.dropdown_frame, text="입차").grid(row=0, column=0, padx=5)
        self.entry_hour = ttk.Combobox(
            self.dropdown_frame,
            values=hour_values,
            width=3,
            state="readonly",
        )
        self.entry_hour.grid(row=0, column=1)
        ttk.Label(self.dropdown_frame, text=":").grid(row=0, column=2)
        self.entry_minute = ttk.Combobox(
            self.dropdown_frame,
            values=minute_values,
            width=3,
            state="readonly",
        )
        self.entry_minute.grid(row=0, column=3, padx=(0, 25))

        ttk.Label(self.dropdown_frame, text="출차").grid(row=0, column=4, padx=5)
        self.exit_hour = ttk.Combobox(
            self.dropdown_frame,
            values=hour_values,
            width=3,
            state="readonly",
        )
        self.exit_hour.grid(row=0, column=5)
        ttk.Label(self.dropdown_frame, text=":").grid(row=0, column=6)
        self.exit_minute = ttk.Combobox(
            self.dropdown_frame,
            values=minute_values,
            width=3,
            state="readonly",
        )
        self.exit_minute.grid(row=0, column=7)

        # Default dropdown values
        self.entry_hour.set("09")
        self.entry_minute.set("00")
        self.exit_hour.set("10")
        self.exit_minute.set("00")

        # Calculate button
        calculate_button = ttk.Button(
            input_frame,
            text="계산 및 등록",
            command=self.add_parking_record,
        )
        calculate_button.pack(pady=(12, 0))

    def change_input_mode(self):
        # Hide both input areas first
        self.manual_frame.pack_forget()
        self.dropdown_frame.pack_forget()

        # Show selected input area
        if self.input_mode.get() == "manual":
            self.manual_frame.pack()
            self.entry_time.focus_set()
        else:
            self.dropdown_frame.pack()

    def auto_input_colon(self, input_box):
        # Keep only four number characters
        input_text = input_box.get()
        number_text = ""

        for character in input_text:
            if character.isdigit():
                number_text = number_text + character

        number_text = number_text[:4]

        # Add colon after hour value
        if len(number_text) >= 3:
            result_text = number_text[:2] + ":" + number_text[2:]
        else:
            result_text = number_text

        # Update entry only when text is changed
        if input_box.get() != result_text:
            input_box.delete(0, tk.END)
            input_box.insert(0, result_text)
            input_box.icursor(tk.END)

    def get_input_times(self):
        # Read manual input
        if self.input_mode.get() == "manual":
            entry_value = self.entry_time.get().strip()
            exit_value = self.exit_time.get().strip()
            return entry_value, exit_value

        # Read dropdown input
        entry_value = self.entry_hour.get() + ":" + self.entry_minute.get()
        exit_value = self.exit_hour.get() + ":" + self.exit_minute.get()
        return entry_value, exit_value

    def add_parking_record(self):
        entry_value, exit_value = self.get_input_times()

        # Check empty input
        if entry_value == "" or exit_value == "":
            messagebox.showwarning("입력 오류", "모든 시간을 입력해주세요")
            return

        # Calculate parking fee
        try:
            self.calculator.calculate_parking(entry_value, exit_value)
        except ValueError as error:
            messagebox.showerror("입력 오류", str(error))
            return

        # Refresh screen
        self.update_record_list()

    # ========================================
    # 3. Parking Record Area
    # ========================================
    def make_record_area(self):
        record_group = ttk.LabelFrame(self.root, text="오늘의 주차 기록", padding=8)
        record_group.pack(fill="both", expand=True, padx=12, pady=6)

        # Header row
        header_frame = ttk.Frame(record_group)
        header_frame.pack(fill="x", padx=(0, 16))

        header_names = ["입차", "출차", "주차 시간", "요금", "삭제"]

        for column_number, header_name in enumerate(header_names):
            header_label = ttk.Label(
                header_frame,
                text=header_name,
                anchor="center",
            )
            header_label.grid(
                row=0,
                column=column_number,
                sticky="ew",
                padx=3,
                pady=3,
            )

            if column_number == 2:
                header_frame.columnconfigure(column_number, weight=2)
            else:
                header_frame.columnconfigure(column_number, weight=1)

        # Scrollable record list
        list_frame = ttk.Frame(record_group)
        list_frame.pack(fill="both", expand=True)

        self.record_canvas = tk.Canvas(list_frame, highlightthickness=0)
        record_scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.record_canvas.yview,
        )

        self.record_rows = ttk.Frame(self.record_canvas)
        self.record_window = self.record_canvas.create_window(
            (0, 0),
            window=self.record_rows,
            anchor="nw",
        )

        self.record_canvas.configure(yscrollcommand=record_scrollbar.set)
        self.record_rows.bind("<Configure>", self.change_scroll_area)
        self.record_canvas.bind("<Configure>", self.change_record_width)

        self.record_canvas.pack(side="left", fill="both", expand=True)
        record_scrollbar.pack(side="right", fill="y")

    def update_record_list(self):
        # Remove old screen rows
        for child_widget in self.record_rows.winfo_children():
            child_widget.destroy()

        all_records = self.calculator.get_all_records()

        # Show empty message
        if len(all_records) == 0:
            empty_label = ttk.Label(
                self.record_rows,
                text="등록된 주차 기록이 없습니다.",
                anchor="center",
            )
            empty_label.pack(fill="x", pady=20)
        else:
            # Make one screen row for each record
            for record_index, record in enumerate(all_records):
                self.make_record_row(record_index, record)

        # Update total fee
        total_fee = self.calculator.get_total_sum()
        self.total_label.config(text=f"오늘의 총 합계: {total_fee:,}원")

    def make_record_row(self, record_index, record):
        row_frame = ttk.Frame(self.record_rows)
        row_frame.pack(fill="x", pady=2)

        row_values = [
            record["entry"],
            record["exit"],
            record["duration"],
            f'{record["fee"]:,}원',
        ]

        # Add text values
        for column_number, row_value in enumerate(row_values):
            value_label = ttk.Label(
                row_frame,
                text=row_value,
                anchor="center",
            )
            value_label.grid(
                row=0,
                column=column_number,
                sticky="ew",
                padx=3,
                pady=2,
            )

            if column_number == 2:
                row_frame.columnconfigure(column_number, weight=2)
            else:
                row_frame.columnconfigure(column_number, weight=1)

        # Add delete button for this row
        delete_button = ttk.Button(
            row_frame,
            text="삭제",
            command=lambda index=record_index: self.delete_parking_record(index),
        )
        delete_button.grid(row=0, column=4, padx=3, pady=2)
        row_frame.columnconfigure(4, weight=1)

    def delete_parking_record(self, record_index):
        try:
            self.calculator.remove_record(record_index)
        except IndexError:
            messagebox.showerror("삭제 오류", "삭제할 주차 기록이 없습니다.")
            return

        self.update_record_list()

    def change_scroll_area(self, event=None):
        self.record_canvas.configure(scrollregion=self.record_canvas.bbox("all"))

    def change_record_width(self, event):
        self.record_canvas.itemconfigure(self.record_window, width=event.width)

    # ========================================
    # 4. Total Fee Area
    # ========================================
    def make_total_area(self):
        self.total_label = ttk.Label(
            self.root,
            text="오늘의 총 합계: 0원",
            font=("Arial", 14, "bold"),
        )
        self.total_label.pack(pady=(6, 14))


if __name__ == "__main__":
    main_window = tk.Tk()
    parking_app = ParkingApp(main_window)
    main_window.mainloop()