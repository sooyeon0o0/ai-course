"""학점 계산기의 입력 검사와 계산 함수."""


GRADE_POINTS = {
    "A+": 4.5,
    "A0": 4.0,
    "B+": 3.5,
    "B0": 3.0,
    "C+": 2.5,
    "C0": 2.0,
    "D+": 1.5,
    "D0": 1.0,
    "F": 0.0,
}
VALID_CREDITS = (1, 2, 3)


def make_course(name, credits, grade):
    """입력을 검사하고 (과목, 오류 문구)를 돌려준다."""
    cleaned_name = str(name).strip()
    if not cleaned_name:
        return None, "과목 이름을 입력합니다"
    try:
        credit_value = int(credits)
    except (TypeError, ValueError):
        return None, "학점 수는 1, 2, 3 중에서 선택합니다"
    if credit_value not in VALID_CREDITS:
        return None, "학점 수는 1, 2, 3 중에서 선택합니다"
    if grade not in GRADE_POINTS:
        return None, "올바른 성적을 선택합니다"

    return {
        "name": cleaned_name,
        "credits": credit_value,
        "grade": grade,
        "point": GRADE_POINTS[grade],
    }, None


def calculate_gpa(courses):
    """과목 목록에서 총 학점과 평점을 계산한다."""
    total_credits = sum(course["credits"] for course in courses)
    if total_credits == 0:
        return 0, 0.0
    total_points = sum(course["point"] * course["credits"] for course in courses)
    return total_credits, total_points / total_credits


def format_gpa(gpa):
    """평점을 소수점 아래 두 자리로 표시한다."""
    return f"{gpa:.2f}"

