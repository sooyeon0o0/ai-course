"""비밀번호 생성기의 계산 함수."""

import random
import string


SPECIALS = "!@#$%^&*"


def parse_length(text):
    """길이 입력을 검사하고 (길이, 오류 문구)를 돌려준다."""
    cleaned = str(text).strip()
    if not cleaned:
        return None, "길이를 입력합니다"
    try:
        length = int(cleaned)
    except ValueError:
        return None, "길이는 정수로 입력합니다"
    if length < 4 or length > 32:
        return None, "길이는 4 이상 32 이하로 입력합니다"
    return length, None


def generate_password(length, use_upper=False, use_digits=False,
                      use_specials=False, rng=None):
    """선택한 각 문자 종류를 하나 이상 포함하는 비밀번호를 만든다."""
    generator = rng if rng is not None else random
    groups = [string.ascii_lowercase]
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_digits:
        groups.append(string.digits)
    if use_specials:
        groups.append(SPECIALS)

    if length < len(groups):
        raise ValueError("선택한 문자 종류를 모두 포함하기에는 길이가 짧습니다")

    characters = [generator.choice(group) for group in groups]
    pool = "".join(groups)
    characters.extend(generator.choice(pool) for _ in range(length - len(characters)))
    generator.shuffle(characters)
    return "".join(characters)


def password_strength(length, use_upper=False, use_digits=False, use_specials=False):
    """길이와 사용 문자 종류 수로 간단한 강도를 판정한다."""
    group_count = 1 + int(use_upper) + int(use_digits) + int(use_specials)
    if length >= 16 and group_count >= 3:
        return "매우 강함"
    if length >= 12 and group_count >= 3:
        return "강함"
    return "보통"

