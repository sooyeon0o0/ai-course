import random

from logic import judge_guess, make_answer, narrow_range, parse_guess


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


check("작은 추측", judge_guess(50, 70), "더 큽니다")
check("큰 추측", judge_guess(90, 70), "더 작습니다")
check("정답", judge_guess(70, 70), "정답입니다")
check("빈 입력", parse_guess("  "), (None, "숫자를 입력합니다"))
check("문자 입력", parse_guess("abc"), (None, "정수를 입력합니다"))
check("작은 범위 오류", parse_guess("0"), (None, "1부터 100 사이의 숫자를 입력합니다"))
check("큰 범위 오류", parse_guess("101"), (None, "1부터 100 사이의 숫자를 입력합니다"))
check("정상 입력", parse_guess(" 42 "), (42, None))
check("아래 범위 좁히기", narrow_range(1, 100, 40, "더 큽니다"), (41, 100))
check("위 범위 좁히기", narrow_range(41, 100, 80, "더 작습니다"), (41, 79))

answer = make_answer(random.Random(7))
check("무작위 정답 범위", 1 <= answer <= 100, True)

print(f"\n결과: 통과 {passed}개, 실패 {failed}개")
raise SystemExit(1 if failed else 0)

