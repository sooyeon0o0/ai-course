"""용돈 기입장의 입력 검사와 합계 계산 함수."""


VALID_KINDS = ("수입", "지출")


def make_entry(description, amount_text, kind):
    """입력을 검사하고 (거래, 오류 문구)를 돌려준다."""
    cleaned_description = str(description).strip()
    if not cleaned_description:
        return None, "내용을 입력합니다"

    cleaned_amount = str(amount_text).strip().replace(",", "")
    if not cleaned_amount:
        return None, "금액을 입력합니다"
    try:
        amount = int(cleaned_amount)
    except ValueError:
        return None, "금액은 0보다 큰 정수로 입력합니다"
    if amount <= 0:
        return None, "금액은 0보다 큰 정수로 입력합니다"
    if kind not in VALID_KINDS:
        return None, "구분은 수입 또는 지출이어야 합니다"

    return {"description": cleaned_description, "amount": amount, "kind": kind}, None


def calculate_totals(entries):
    """거래 목록에서 수입, 지출, 잔액을 계산한다."""
    income = sum(entry["amount"] for entry in entries if entry["kind"] == "수입")
    expense = sum(entry["amount"] for entry in entries if entry["kind"] == "지출")
    return income, expense, income - expense


def format_won(amount):
    """정수를 쉼표가 들어간 원화 문자열로 바꾼다."""
    return f"{amount:,}원"

