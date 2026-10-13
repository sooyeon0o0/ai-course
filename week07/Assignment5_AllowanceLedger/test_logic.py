from logic import calculate_totals, format_won, make_entry


passed = 0
failed = 0


def check(name, actual, expected):
    global passed, failed
    if actual == expected:
        passed += 1
        print(f"통과: {name}")
    else:
        failed += 1
        print(f"실패: {name} / 기대={expected!r}, 실제={actual!r}")


income, error = make_entry(" 용돈 ", "10,000", "수입")
check("수입 입력 오류 없음", error, None)
check("수입 입력 정리", income, {"description": "용돈", "amount": 10000, "kind": "수입"})

expense, error = make_entry("간식", "2,500", "지출")
check("지출 입력 오류 없음", error, None)
check("쉼표 금액", expense["amount"], 2500)
check("빈 내용", make_entry(" ", "1000", "수입"), (None, "내용을 입력합니다"))
check("빈 금액", make_entry("용돈", "", "수입"), (None, "금액을 입력합니다"))
check("0원", make_entry("용돈", "0", "수입")[0], None)
check("음수", make_entry("용돈", "-1", "수입")[0], None)
check("문자 금액", make_entry("용돈", "abc", "수입")[0], None)
check("소수 금액", make_entry("용돈", "1.5", "수입")[0], None)
check("잘못된 구분", make_entry("용돈", "1000", "기타")[0], None)
check("합계", calculate_totals([income, expense]), (10000, 2500, 7500))
check("금액 표시", format_won(1234567), "1,234,567원")
check("음수 표시", format_won(-2500), "-2,500원")

print(f"\n결과: 통과 {passed}개, 실패 {failed}개")
raise SystemExit(1 if failed else 0)

