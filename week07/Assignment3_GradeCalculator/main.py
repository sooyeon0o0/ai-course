import flet as ft

from logic import GRADE_POINTS, calculate_gpa, format_gpa, make_course


def main(page: ft.Page):
    page.title = "학점 계산기"
    page.window.width = 520
    page.window.height = 680
    page.window.resizable = False

    courses = []

    name_input = ft.TextField(label="과목 이름", value="", width=220)
    credits_input = ft.Dropdown(
        label="학점 수",
        value="3",
        width=110,
        options=[ft.dropdown.Option("1"), ft.dropdown.Option("2"), ft.dropdown.Option("3")],
    )
    grade_input = ft.Dropdown(
        label="성적",
        value="A+",
        width=110,
        options=[ft.dropdown.Option(grade) for grade in GRADE_POINTS],
    )
    total_text = ft.Text(value="총 학점: 0", weight=ft.FontWeight.BOLD)
    gpa_text = ft.Text(value="평점: 0.00", size=20, weight=ft.FontWeight.BOLD)
    count_text = ft.Text(value="과목 수: 0개")
    notice = ft.Text(value="", color=ft.Colors.RED)
    items = ft.ListView(expand=True, spacing=4)

    def refresh():
        total_credits, gpa = calculate_gpa(courses)
        total_text.value = f"총 학점: {total_credits}"
        gpa_text.value = f"평점: {format_gpa(gpa)}"
        count_text.value = f"과목 수: {len(courses)}개"
        items.controls.clear()
        for index, course in enumerate(courses):
            items.controls.append(ft.Row(controls=[
                ft.Text(
                    value=f"{course['name']} / {course['credits']}학점 / {course['grade']}",
                    expand=True,
                ),
                ft.Button(content="삭제", data=index, on_click=on_delete),
            ]))

    def on_add(e):
        notice.value = ""
        course, error = make_course(name_input.value, credits_input.value, grade_input.value)
        if error:
            notice.value = error
        else:
            courses.append(course)
            name_input.value = ""
            refresh()
        page.update()

    def on_delete(e):
        courses.pop(e.control.data)
        notice.value = ""
        refresh()
        page.update()

    page.add(
        ft.Text(value="학점 계산기", size=28, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[name_input]),
        ft.Row(controls=[credits_input, grade_input]),
        ft.Button(content="추가", on_click=on_add, expand=True, height=44,
                  bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        notice,
        ft.Row(controls=[total_text, gpa_text]),
        count_text,
        items,
    )


ft.run(main)

