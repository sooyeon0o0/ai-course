"""숫자 맞히기의 계산과 판정 함수."""

import random


def make_answer(rng=None):
    """1부터 100 사이의 무작위 정답을 만든다."""
    generator = rng if rng is not None else random
    return generator.randint(1, 100)


def parse_guess(text):
    """입력 문자열을 검사하고 (숫자, 오류 문구)를 돌려준다."""
    cleaned = str(text).strip()
    if not cleaned:
        return None, "숫자를 입력합니다"
    try:
        guess = int(cleaned)
    except ValueError:
        return None, "정수를 입력합니다"
    if guess < 1 or guess > 100:
        return None, "1부터 100 사이의 숫자를 입력합니다"
    return guess, None


def judge_guess(guess, answer):
    """추측값과 정답을 비교한다."""
    if guess < answer:
        return "더 큽니다"
    if guess > answer:
        return "더 작습니다"
    return "정답입니다"


def narrow_range(low, high, guess, judgment):
    """판정에 따라 가능한 정답 범위를 좁힌다."""
    if judgment == "더 큽니다":
        low = max(low, guess + 1)
    elif judgment == "더 작습니다":
        high = min(high, guess - 1)
    return low, high

