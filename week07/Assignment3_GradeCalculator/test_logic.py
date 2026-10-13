from logic import GRADE_POINTS, calculate_gpa, format_gpa, make_course


passed = 0
failed = 0


def check(name, actual, expected, tolerance=None):
    global passed, failed
    same = abs(actual - expected) < tolerance if tolerance is not None else actual == expected
    if same:
        passed += 1
        print(f"통과: {name}")
    else:
        failed += 1
        print(f"실패: {name} / 기대={expected!r}, 실제={actual!r}")


course_a, error = make_course(" 자료구조 ", "3", "A+")
check("정상 과목 오류 없음", error, None)
check("과목 이름 정리", course_a["name"], "자료구조")
check("학점 변환", course_a["credits"], 3)
check("성적 점수", course_a["point"], 4.5)
check("빈 과목 이름", make_course(" ", 3, "A+")[0], None)
check("잘못된 학점 문자", make_course("과목", "abc", "A+")[0], None)
check("0학점", make_course("과목", 0, "A+")[0], None)
check("4학점", make_course("과목", 4, "A+")[0], None)
check("잘못된 성적", make_course("과목", 3, "A")[0], None)
check("성적 종류 수", len(GRADE_POINTS), 9)

course_b, error = make_course("운영체제", 2, "B0")
total_credits, gpa = calculate_gpa([course_a, course_b])
check("총 학점", total_credits, 5)
check("가중 평점", gpa, 3.9, 0.000001)
check("빈 목록", calculate_gpa([]), (0, 0.0))
check("평점 표시", format_gpa(3.9), "3.90")

print(f"\n결과: 통과 {passed}개, 실패 {failed}개")
raise SystemExit(1 if failed else 0)

