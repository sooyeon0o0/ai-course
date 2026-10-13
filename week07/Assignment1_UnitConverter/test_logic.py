from logic import convert_value, format_number, parse_value, unit_kind


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


check("빈 입력", parse_value(" "), (None, "값을 입력합니다"))
check("문자 입력", parse_value("abc"), (None, "숫자를 입력합니다"))
check("정상 입력", parse_value(" 1.5 "), (1.5, None))
check("길이 종류", unit_kind("km"), "길이")
check("온도 종류", unit_kind("°F"), "온도")
check("알 수 없는 단위", unit_kind("inch"), None)

check("cm에서 mm", convert_value(10, "cm", "mm")[0], 100.0, 0.000001)
check("m에서 km", convert_value(1000, "m", "km")[0], 1.0, 0.000001)
check("km에서 m", convert_value(1, "km", "m")[0], 1000.0, 0.000001)
check("섭씨에서 화씨", convert_value(0, "°C", "°F")[0], 32.0, 0.000001)
check("화씨에서 섭씨", convert_value(212, "°F", "°C")[0], 100.0, 0.000001)
check("같은 단위", convert_value(12.5, "cm", "cm"), (12.5, None))
check("종류 혼합", convert_value(1, "m", "°C")[0], None)
check("숫자 표시", format_number(12.340000), "12.34")
check("정수 표시", format_number(100.0), "100")

print(f"\n결과: 통과 {passed}개, 실패 {failed}개")
raise SystemExit(1 if failed else 0)

