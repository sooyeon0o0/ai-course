import flet as ft

from logic import generate_password, parse_length, password_strength


def main(page: ft.Page):
    page.title = "비밀번호 생성기"
    page.window.width = 430
    page.window.height = 520
    page.window.resizable = False

    length_input = ft.TextField(label="길이 (4~32)", value="12", width=180)
    upper = ft.Checkbox(label="대문자 포함", value=True)
    digits = ft.Checkbox(label="숫자 포함", value=True)
    specials = ft.Checkbox(label="특수문자 포함 (!@#$%^&*)", value=True)
    result = ft.Text(value="", size=22, weight=ft.FontWeight.BOLD)
    strength = ft.Text(value="")
    notice = ft.Text(value="", color=ft.Colors.RED)

    def on_generate(e):
        notice.value = ""
        result.value = ""
        strength.value = ""
        length, error = parse_length(length_input.value)
        if error:
            notice.value = error
        else:
            result.value = generate_password(
                length,
                use_upper=upper.value,
                use_digits=digits.value,
                use_specials=specials.value,
            )
            level = password_strength(length, upper.value, digits.value, specials.value)
            strength.value = f"비밀번호 강도: {level}"
        page.update()

    page.add(
        ft.Text(value="비밀번호 생성기", size=28, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[length_input]),
        upper,
        digits,
        specials,
        ft.Button(content="비밀번호 만들기", on_click=on_generate, expand=True, height=44,
                  bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        result,
        strength,
        notice,
    )


ft.run(main)

