def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! 0으로 나눌 수 없습니다."
    return x / y

def calculator():
    print("=== 파이썬 계산기 프로그램을 시작합니다 ===")
    print("사용 가능한 연산자: +, -, *, /")
    print("종료하려면 'q'를 입력하세요.")

    while True:
        print("\n--------------------------------")
        user_input = input("계산할 첫 번째 숫자를 입력하세요 (종료: q): ").strip().lower()
        
        if user_input == 'q':
            print("계산기를 종료합니다. 이용해 주셔서 감사합니다!")
            break

        try:
            num1 = float(user_input)
            
            operator = input("연산자를 입력하세요 (+, -, *, /): ").strip()
            if operator not in ['+', '-', '*', '/']:
                print("잘못된 연산자입니다. 다시 시도해주세요.")
                continue

            num2 = input("두 번째 숫자를 입력하세요: ").strip()
            if num2.lower() == 'q':
                print("계산기를 종료합니다.")
                break
            num2 = float(num2)

            # 연산 수행
            if operator == '+':
                result = add(num1, num2)
            elif operator == '-':
                result = subtract(num1, num2)
            elif operator == '*':
                result = multiply(num1, num2)
            elif operator == '/':
                result = divide(num1, num2)

            # 결과 출력
            print(f"\n👉 결과: {num1} {operator} {num2} = {result}")

        except ValueError:
            print("❌ 오류: 올바른 숫자를 입력해주세요.")
        except Exception as e:
            print(f"❌ 알 수 없는 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    calculator()
