import flet as ft

from logic import judge_guess, make_answer, narrow_range, parse_guess


def main(page: ft.Page):
    page.title = "숫자 맞히기"
    page.window.width = 420
    page.window.height = 620
    page.window.resizable = False

    answer = make_answer()
    attempts = 0
    low = 1
    high = 100
    finished = False

    guess_input = ft.TextField(label="1~100 사이의 숫자", value="", width=240)
    count_text = ft.Text(value="시도 횟수: 0", size=18, weight=ft.FontWeight.BOLD)
    range_text = ft.Text(value="가능한 범위: 1~100")
    result = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    notice = ft.Text(value="", color=ft.Colors.RED)
    history = ft.ListView(expand=True, spacing=4)

    def on_guess(e):
        nonlocal attempts, low, high, finished
        notice.value = ""
        if finished:
            notice.value = "새 게임 버튼을 눌러 주세요"
            page.update()
            return

        guess, error = parse_guess(guess_input.value)
        if error:
            notice.value = error
            page.update()
            return

        judgment = judge_guess(guess, answer)
        attempts += 1
        count_text.value = f"시도 횟수: {attempts}"
        history.controls.append(ft.Row(controls=[
            ft.Text(value=f"{guess} - {judgment}", expand=True),
        ]))

        if judgment == "정답입니다":
            finished = True
            result.value = f"정답! {attempts}번 만에 맞혔습니다"
        else:
            low, high = narrow_range(low, high, guess, judgment)
            result.value = judgment
            range_text.value = f"가능한 범위: {low}~{high}"

        guess_input.value = ""
        page.update()

    def on_new_game(e):
        nonlocal answer, attempts, low, high, finished
        answer = make_answer()
        attempts = 0
        low = 1
        high = 100
        finished = False
        guess_input.value = ""
        count_text.value = "시도 횟수: 0"
        range_text.value = "가능한 범위: 1~100"
        result.value = ""
        notice.value = "새 게임을 시작합니다"
        history.controls.clear()
        page.update()

    page.add(
        ft.Text(value="숫자 맞히기", size=28, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[guess_input]),
        ft.Row(controls=[
            ft.Button(content="확인", on_click=on_guess, expand=True, height=44,
                      bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
            ft.Button(content="새 게임", on_click=on_new_game, expand=True, height=44),
        ]),
        count_text,
        range_text,
        result,
        notice,
        history,
    )


ft.run(main)

