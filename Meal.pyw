# Editor : I love dormitory cafeteria !
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from datetime import datetime

# URL 설정
url = 'https://dormitory.jnu.ac.kr/Board/Board.aspx?BoardID=2'

# GET 요청으로 페이지 가져오기
response = requests.get(url)

# 요청이 성공했는지 확인 
if response.status_code == 200:
    # 페이지 내용 파싱
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 식단표를 찾는 부분 
    menu_table = soup.find('table')  
    
    # 식단 내용 추출
    menu = []
    for row in menu_table.find_all('tr'):
        columns = row.find_all('td')
        menu.append([column.get_text(strip=True) for column in columns])
        
       
    # 요일별 식사 변수 설정
    # 월요일부터 일요일까지
    weekly_menu = {
        "월요일": {
            "breakfast": menu[1][0],
            "lunch A": menu[2][0],
            "lunch B": menu[3][0],
            "dinner" : menu[4][0]
        },
        "화요일": {
            "breakfast": menu[1][1],
            "lunch A": menu[2][1],
            "lunch B": menu[3][1],
            "dinner" : menu[4][1]
        },
        "수요일": {
            "breakfast": menu[1][2],
            "lunch A": menu[2][2],
            "lunch B": menu[3][2],
            "dinner" : menu[4][2]
        },
        "목요일": {
            "breakfast": menu[1][3],
            "lunch A": menu[2][3],
            "lunch B": menu[3][3],
            "dinner" : menu[4][3]
        },
        "금요일": {
            "breakfast": menu[1][4],
            "lunch A": menu[2][4],
            "lunch B": menu[3][4],
            "dinner" : menu[4][4]
        },
        "토요일": {
            "breakfast": menu[1][5],
            "lunch A": menu[2][5],
            "lunch B": menu[3][5],
            "dinner" : menu[4][5]
        },
        "일요일": {
            "breakfast": menu[1][6],
            "lunch A": menu[2][6],
            "lunch B": menu[3][6],
            "dinner" : menu[4][6]
        }
    }

    # 현재 요일 가져오기
    current_weekday = datetime.now().strftime("%A")  # "Monday", "Tuesday", ...
    
    # 요일 한글로 변환
    korean_weekdays = {
        "Monday": "월요일",
        "Tuesday": "화요일",
        "Wednesday": "수요일",
        "Thursday": "목요일",
        "Friday": "금요일",
        "Saturday": "토요일",
        "Sunday": "일요일"
    }

    current_korean_weekday = korean_weekdays[current_weekday]

    # tkinter 기본 창 숨기기
    root = tk.Tk()
    root.withdraw()  

    # 사용자 정의 경고창 생성
    def show_custom_warning(message):
        custom_warning = tk.Toplevel(root)  # root를 부모로 설정
        custom_warning.title("식단 알림")
        
        # 라벨 생성 및 설정
        label = tk.Label(custom_warning, text=message, font=("Arial", 20))  # 글씨 크기 조정
        label.pack(padx=30, pady=30)

        # 확인 버튼 생성 (글자 크기 조정)
        button = tk.Button(custom_warning, text="확인", command=root.quit, 
                           width=8, height=1, font=("Arial", 25))  # root.quit로 변경
        button.pack(pady=20)

        custom_warning.mainloop()

    # 현재 요일의 메뉴 가져오기
    today_menu = weekly_menu[current_korean_weekday]
    menu_message = (f"!!! {current_korean_weekday} 긱식 !!!\n"
                    f"\n<---아침--->\n {today_menu['breakfast']}\n"
                    f"\n<---점심A--->\n {today_menu['lunch A']}\n"
                    f"\n<---점심B--->\n {today_menu['lunch B']}\n"
                    f"\n<---저녁--->\n {today_menu['dinner']}")

    show_custom_warning(menu_message)

else:
    print("페이지를 불러올 수 없습니다. 상태 코드:", response.status_code)
