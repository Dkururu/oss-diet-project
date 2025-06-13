import json
import os
from datetime import datetime

DATA_FILE = 'diet_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'weight_history': [], 'meals': {}, 'goal': {}, 'exercise': {}}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calc_goal_calories(std_weight, weekly_loss):
    return int(std_weight * 30 - weekly_loss * 7)

def set_goal(data):
    height = float(input("키(cm): ")) / 100
    curr_weight = float(input("현재 몸무게(kg): "))
    weekly_loss = float(input("일주일간 감량 목표(kg): "))
    std_weight = height ** 2 * 22
    goal_kcal = calc_goal_calories(std_weight, weekly_loss)
    print(f"표준체중: {std_weight:.2f}kg / 목표 섭취 칼로리: {goal_kcal}kcal")
    data['goal'] = {
        'height': height,
        'std_weight': std_weight,
        'weekly_loss': weekly_loss,
        'goal_kcal': goal_kcal
    }
    today = datetime.today().strftime('%Y-%m-%d')
    data['weight_history'].append({'date': today, 'weight': curr_weight})
    save_data(data)

def add_meal(data):
    today = datetime.today().strftime('%Y-%m-%d')
    if today not in data['meals']:
        data['meals'][today] = []
    name = input("음식명: ")
    kcal = int(input("칼로리: "))
    data['meals'][today].append({'name': name, 'kcal': kcal})
    save_data(data)
    print("식단이 추가되었습니다.")

def del_meal(data):
    today = datetime.today().strftime('%Y-%m-%d')
    meals = data['meals'].get(today, [])
    if not meals:
        print("오늘 식단이 없습니다.")
        return
    for idx, m in enumerate(meals):
        print(f"{idx+1}. {m['name']} - {m['kcal']}kcal")
    num = int(input("삭제할 번호: ")) - 1
    if 0 <= num < len(meals):
        removed = meals.pop(num)
        print(f"{removed['name']} 삭제됨")
        data['meals'][today] = meals
        save_data(data)
    else:
        print("잘못된 번호입니다.")

def show_meals(data):
    today = datetime.today().strftime('%Y-%m-%d')
    meals = data['meals'].get(today, [])
    if not meals:
        print("오늘 식단이 없습니다.")
    else:
        for m in meals:
            print(f"- {m['name']} : {m['kcal']}kcal")

def add_weight(data):
    today = datetime.today().strftime('%Y-%m-%d')
    weight = float(input("현재 몸무게(kg): "))
    data['weight_history'].append({'date': today, 'weight': weight})
    save_data(data)
    print("몸무게가 기록되었습니다.")

def show_weight_graph(data):
    history = data['weight_history']
    if not history:
        print("몸무게 기록이 없습니다.")
        return
    print("몸무게 변화 추이:")
    min_w = min([w['weight'] for w in history])
    for entry in history:
        date = entry['date']
        w = entry['weight']
        bar = '▇' * int((w-min_w+1)*3)
        print(f"{date} {w:.1f}kg {bar}")

def show_summary(data):
    today = datetime.today().strftime('%Y-%m-%d')
    meals = data['meals'].get(today, [])
    intake = sum(m['kcal'] for m in meals)
    goal = data['goal'].get('goal_kcal', 2000)
    burn = 0 # 운동/소모 추가 가능
    remain = goal - intake + burn
    print(f"오늘 목표 칼로리: {goal}kcal")
    print(f"섭취 칼로리: {intake}kcal")
    print(f"소모 칼로리: {burn}kcal")
    print(f"남은 칼로리: {remain}kcal")

def main():
    data = load_data()
    while True:
        os.system('cls')
        print("\n[다이어트 보조 프로그램]")
        print("1. 식단 관리")
        print("2. 몸무게/칼로리 관리")
        print("3. 목표 칼로리/몸무게 설정")
        print("0. 종료")
        menu = input("메뉴 선택: ")
        if menu == '1':
            while True:
                print("\n[식단 관리]")
                print("1. 오늘의 식단 추가")
                print("2. 오늘의 식단 삭제")
                print("3. 오늘의 식단 조회")
                print("0. 뒤로가기")
                sub = input("메뉴 선택: ")
                if sub == '1': add_meal(data)
                elif sub == '2': del_meal(data)
                elif sub == '3': show_meals(data)
                elif sub == '0': break
                else: print("잘못된 입력입니다.")
        elif menu == '2':
            while True:
                print("\n[몸무게/칼로리 관리]")
                print("1. 몸무게 기록")
                print("2. 몸무게 변화 추이")
                print("3. 오늘 칼로리 요약")
                print("0. 뒤로가기")
                sub = input("메뉴 선택: ")
                if sub == '1': add_weight(data)
                elif sub == '2': show_weight_graph(data)
                elif sub == '3': show_summary(data)
                elif sub == '0': break
                else: print("잘못된 입력입니다.")
        elif menu == '3': set_goal(data)
        elif menu == '0': break
        else: print("잘못된 입력입니다.")


if __name__ == '__main__':
    main()
