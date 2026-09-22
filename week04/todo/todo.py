import json
import os
from datetime import datetime

DATA_FILE = "todo.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def get_sorted_tasks(tasks):
    """Return tasks sorted by deadline (earliest first)."""
    # 마감일이 없는 경우(None)를 위해 아주 먼 미래의 날짜로 처리하여 정렬
    return sorted(
        tasks, 
        key=lambda x: x.get("deadline") if x.get("deadline") else "9999-12-31"
    )

def show_tasks(tasks):
    """Display the list of tasks, sorted by deadline."""
    print("\n--- 할 일 목록 (마감일 순) ---")
    if not tasks:
        print("할 일이 없습니다.")
    else:
        sorted_tasks = get_sorted_tasks(tasks)
        for i, task in enumerate(sorted_tasks, 1):
            status = "[V]" if task["completed"] else "[ ]"
            deadline = task.get("deadline") if task.get("deadline") else "기한 없음"
            print(f"{i}. {status} {task['task']} (마감: {deadline})")
    print("----------------------------")

def add_task(tasks):
    """Add a new task with a deadline."""
    task_name = input("추가할 할 일을 입력하세요: ").strip()
    if not task_name:
        print("할 일 내용은 비워둘 수 없습니다.")
        return

    deadline = input("마감일을 입력하세요 (YYYY-MM-DD, 미입력 시 건너뜀): ").strip()
    
    if deadline:
        try:
            # 날짜 형식 검증
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            print("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요. 마감일 없이 추가합니다.")
            deadline = None

    tasks.append({
        "task": task_name,
        "completed": False,
        "deadline": deadline
    })
    print(f"'{task_name}'(이)가 추가되었습니다.")

def complete_task(tasks):
    """Mark a task as completed."""
    show_tasks(tasks)
    if not tasks:
        return
    
    sorted_tasks = get_sorted_tasks(tasks)
    
    try:
        num = int(input("완료 처리할 번호를 입력하세요: "))
        if 1 <= num <= len(sorted_tasks):
            target_task = sorted_tasks[num-1]
            # 원본 tasks 리스트에서 해당 항목을 찾아 업데이트
            for task in tasks:
                if task == target_task:
                    task["completed"] = True
                    break
            print(f"{num}번 할 일을 완료 처리했습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def delete_task(tasks):
    """Delete a task."""
    show_tasks(tasks)
    if not tasks:
        return

    sorted_tasks = get_sorted_tasks(tasks)

    try:
        num = int(input("삭제할 번호를 입력하세요: "))
        if 1 <= num <= len(sorted_tasks):
            target_task = sorted_tasks[num-1]
            tasks.remove(target_task)
            print(f"'{target_task['task']}'(이)가 삭제되었습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def main():
    tasks = load_tasks()
    
    while True:
        print("\n[ To-Do 리스트 메뉴 ]")
        print("1. 목록 보기")
        print("2. 할 일 추가")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("원하는 메뉴 번호를 선택하세요: ").strip()
        
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
            save_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
            save_tasks(tasks)
        elif choice == "4":
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == "5":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
