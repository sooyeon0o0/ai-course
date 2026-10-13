"""단위 변환기의 입력 검사와 계산 함수."""


LENGTH_FACTORS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}
TEMPERATURE_UNITS = ("°C", "°F")
ALL_UNITS = tuple(LENGTH_FACTORS) + TEMPERATURE_UNITS


def parse_value(text):
    """입력 문자열을 실수로 바꿔 (값, 오류 문구)를 돌려준다."""
    cleaned = str(text).strip()
    if not cleaned:
        return None, "값을 입력합니다"
    try:
        return float(cleaned), None
    except ValueError:
        return None, "숫자를 입력합니다"


def unit_kind(unit):
    """단위의 종류를 돌려준다."""
    if unit in LENGTH_FACTORS:
        return "길이"
    if unit in TEMPERATURE_UNITS:
        return "온도"
    return None


def convert_value(value, from_unit, to_unit):
    """값을 변환해 (결과, 오류 문구)를 돌려준다."""
    from_kind = unit_kind(from_unit)
    to_kind = unit_kind(to_unit)
    if from_kind is None or to_kind is None:
        return None, "올바른 단위를 선택합니다"
    if from_kind != to_kind:
        return None, "길이와 온도 단위는 서로 변환할 수 없습니다"
    if from_unit == to_unit:
        return float(value), None

    if from_kind == "길이":
        meters = value * LENGTH_FACTORS[from_unit]
        return meters / LENGTH_FACTORS[to_unit], None

    if from_unit == "°C" and to_unit == "°F":
        return value * 9 / 5 + 32, None
    return (value - 32) * 5 / 9, None


def format_number(value):
    """소수점 아래 최대 6자리로 값을 표시한다."""
    text = f"{value:.6f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text

