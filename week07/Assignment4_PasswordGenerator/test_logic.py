import random
import string

from logic import SPECIALS, generate_password, parse_length, password_strength


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


check("빈 길이", parse_length(""), (None, "길이를 입력합니다"))
check("문자 길이", parse_length("abc"), (None, "길이는 정수로 입력합니다"))
check("최솟값 미만", parse_length("3"), (None, "길이는 4 이상 32 이하로 입력합니다"))
check("최댓값 초과", parse_length("33"), (None, "길이는 4 이상 32 이하로 입력합니다"))
check("정상 길이", parse_length(" 12 "), (12, None))

lower_only = generate_password(4, rng=random.Random(1))
check("소문자 전용 길이", len(lower_only), 4)
check("소문자 전용 구성", all(ch in string.ascii_lowercase for ch in lower_only), True)

all_types = generate_password(12, True, True, True, random.Random(2))
check("전체 선택 길이", len(all_types), 12)
check("소문자 포함", any(ch in string.ascii_lowercase for ch in all_types), True)
check("대문자 포함", any(ch in string.ascii_uppercase for ch in all_types), True)
check("숫자 포함", any(ch in string.digits for ch in all_types), True)
check("특수문자 포함", any(ch in SPECIALS for ch in all_types), True)
check("강도-강함", password_strength(12, True, True, True), "강함")
check("강도-매우 강함", password_strength(16, True, True, True), "매우 강함")

print(f"\n결과: 통과 {passed}개, 실패 {failed}개")
raise SystemExit(1 if failed else 0)

