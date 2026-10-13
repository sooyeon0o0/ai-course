import flet as ft

from logic import ALL_UNITS, convert_value, format_number, parse_value


def main(page: ft.Page):
    page.title = "단위 변환기"
    page.window.width = 500
    page.window.height = 620
    page.window.resizable = False

    value_input = ft.TextField(label="값", value="", width=160)
    from_unit = ft.Dropdown(
        label="출발 단위",
        value="cm",
        width=130,
        options=[ft.dropdown.Option(unit) for unit in ALL_UNITS],
    )
    to_unit = ft.Dropdown(
        label="도착 단위",
        value="m",
        width=130,
        options=[ft.dropdown.Option(unit) for unit in ALL_UNITS],
    )
    result = ft.Text(value="", size=22, weight=ft.FontWeight.BOLD)
    notice = ft.Text(value="", color=ft.Colors.RED)
    history = ft.ListView(expand=True, spacing=4)

    def on_convert(e):
        notice.value = ""
        result.value = ""
        value, error = parse_value(value_input.value)
        if error:
            notice.value = error
            page.update()
            return

        converted, error = convert_value(value, from_unit.value, to_unit.value)
        if error:
            notice.value = error
        else:
            source_text = format_number(value)
            result_text = format_number(converted)
            result.value = f"{result_text} {to_unit.value}"
            history.controls.append(ft.Row(controls=[
                ft.Text(
                    value=f"{source_text} {from_unit.value} → {result_text} {to_unit.value}",
                    expand=True,
                ),
                ft.Button(content="삭제", data=len(history.controls), on_click=on_delete),
            ]))
        page.update()

    def on_delete(e):
        history.controls.pop(e.control.data)
        for index, row in enumerate(history.controls):
            row.controls[1].data = index
        page.update()

    page.add(
        ft.Text(value="단위 변환기", size=28, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[value_input]),
        ft.Row(controls=[from_unit, to_unit]),
        ft.Button(content="변환", on_click=on_convert, expand=True, height=44,
                  bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        result,
        notice,
        ft.Text(value="변환 기록", weight=ft.FontWeight.BOLD),
        history,
    )


ft.run(main)

