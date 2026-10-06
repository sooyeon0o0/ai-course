import re

def format_phone_number(phone_str):
    # 1. 숫자만 남기기
    digits = re.sub(r'\D', '', phone_str)
    length = len(digits)
    
    # 2. 시작 번호 확인
    if digits.startswith('010'):
        if length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 010 번호 형식입니다."

    elif digits.startswith(('011', '016', '017', '018', '019')):
        if length == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif length == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        else:
            return "잘못된 구형 번호 형식입니다."
            
    else:
        return "유효하지 않은 시작 번호입니다."

# --- 테스트 ---
test_cases = [
    "01012345678",    # 010 (11자리) -> 010-1234-5678
    "0111234567",     # 011 (10자리) -> 011-123-4567
    "01612345678",    # 016 (11자리) -> 016-1234-5678
    "0101234567",     # 010 (10자리) -> 에러
    "01912345678",    # 019 (11자리) -> 019-1234-5678
    "0212345678"      # 유효하지 않음
]

for tc in test_cases:
    print(f"{tc} => {format_phone_number(tc)}")
