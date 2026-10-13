import flet as ft

from logic import calculate_totals, format_won, make_entry


def main(page: ft.Page):
    page.title = "용돈 기입장"
    page.window.width = 520
    page.window.height = 680
    page.window.resizable = False

    entries = []

    description_input = ft.TextField(label="내용", value="", width=190)
    amount_input = ft.TextField(label="금액", value="", width=150)
    kind_input = ft.Dropdown(
        label="구분",
        value="지출",
        width=110,
        options=[ft.dropdown.Option("수입"), ft.dropdown.Option("지출")],
    )
    income_text = ft.Text(value="수입 합계: 0원", weight=ft.FontWeight.BOLD)
    expense_text = ft.Text(value="지출 합계: 0원", weight=ft.FontWeight.BOLD)
    balance_text = ft.Text(value="잔액: 0원", size=20, weight=ft.FontWeight.BOLD)
    count_text = ft.Text(value="거래 건수: 0건")
    notice = ft.Text(value="", color=ft.Colors.RED)
    items = ft.ListView(expand=True, spacing=4)

    def refresh():
        income, expense, balance = calculate_totals(entries)
        income_text.value = f"수입 합계: {format_won(income)}"
        expense_text.value = f"지출 합계: {format_won(expense)}"
        balance_text.value = f"잔액: {format_won(balance)}"
        count_text.value = f"거래 건수: {len(entries)}건"
        items.controls.clear()
        for index, entry in enumerate(entries):
            items.controls.append(ft.Row(controls=[
                ft.Text(
                    value=f"[{entry['kind']}] {entry['description']}  {format_won(entry['amount'])}",
                    expand=True,
                ),
                ft.Button(content="삭제", data=index, on_click=on_delete),
            ]))

    def on_add(e):
        notice.value = ""
        entry, error = make_entry(description_input.value, amount_input.value, kind_input.value)
        if error:
            notice.value = error
        else:
            entries.append(entry)
            description_input.value = ""
            amount_input.value = ""
            refresh()
        page.update()

    def on_delete(e):
        entries.pop(e.control.data)
        notice.value = ""
        refresh()
        page.update()

    page.add(
        ft.Text(value="용돈 기입장", size=28, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[description_input, amount_input]),
        ft.Row(controls=[kind_input]),
        ft.Button(content="추가", on_click=on_add, expand=True, height=44,
                  bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        notice,
        ft.Row(controls=[income_text, expense_text]),
        balance_text,
        count_text,
        items,
    )


ft.run(main)

