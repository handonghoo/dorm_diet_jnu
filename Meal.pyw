# Editor : I love dormitory cafeteria !
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from datetime import datetime
import sys

# URL 설정
url = 'https://dormitory.jnu.ac.kr/Board/Board.aspx?BoardID=2'

# GET 요청으로 페이지 가져오기
response = requests.get(url)

# 요청한 내용이 성공적으로 처리되었는지 확인
if response.status_code == 200:
    # 페이지 소스를 BeautifulSoup을 사용해 파싱
    soup = BeautifulSoup(response.content, 'html.parser')

    # 식단표를 포함하는 테이블 찾기
    menu_table = soup.find('table', class_='color')
    

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
        custom_warning = tk.Toplevel(root)
        custom_warning.title("오늘의 식단")
        
        # 창 스타일 설정
        custom_warning.overrideredirect(True)  # 기본 타이틀 바 제거
        
        # 창 크기 설정
        window_width = 700
        window_height = 900
        
        # 화면 중앙에 위치시키기
        screen_width = custom_warning.winfo_screenwidth()
        screen_height = custom_warning.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        custom_warning.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 전체를 감싸는 메인 프레임
        main_container = tk.Frame(custom_warning, bg='white')
        main_container.pack(fill='both', expand=True)
        
        # 커스텀 타이틀 바 프레임
        title_bar = tk.Frame(main_container, bg='#006F3F', height=40)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)
        
        # 타이틀 텍스트
        title_text = tk.Label(title_bar, 
                            text="오늘의 식단",
                            font=("맑은 고딕", 14),
                            bg='#006F3F',
                            fg='white')
        title_text.pack(side='left', padx=15)
        
        # 버튼 프레임 (우측 정렬)
        button_container = tk.Frame(title_bar, bg='#006F3F')
        button_container.pack(side='right')
        
        # 최소화 버튼
        minimize_btn = tk.Label(button_container, 
                              text="─",
                              font=("맑은 고딕", 12),
                              bg='#006F3F',
                              fg='white',
                              cursor='hand2',
                              width=4)
        minimize_btn.pack(side='left')
        minimize_btn.bind('<Button-1>', lambda e: custom_warning.iconify())
        
        # 최대화 버튼
        def toggle_maximize(e):
            if custom_warning.state() == 'zoomed':
                custom_warning.state('normal')
            else:
                custom_warning.state('zoomed')
                
        maximize_btn = tk.Label(button_container, 
                              text="□",
                              font=("맑은 고딕", 12),
                              bg='#006F3F',
                              fg='white',
                              cursor='hand2',
                              width=4)
        maximize_btn.pack(side='left')
        maximize_btn.bind('<Button-1>', toggle_maximize)
        
        # 닫기 버튼
        close_btn = tk.Label(button_container, 
                           text="×",
                           font=("맑은 고딕", 14),
                           bg='#006F3F',
                           fg='white',
                           cursor='hand2',
                           width=4)
        close_btn.pack(side='left')
        close_btn.bind('<Button-1>', lambda e: on_closing())
        
        # 버튼 호버 효과
        def on_enter(event):
            event.widget.configure(bg='#005732')
            
        def on_leave(event):
            event.widget.configure(bg='#006F3F')
            
        for btn in [minimize_btn, maximize_btn, close_btn]:
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # 창 드래그 기능
        def start_move(event):
            custom_warning.x = event.x
            custom_warning.y = event.y

        def stop_move(event):
            custom_warning.x = None
            custom_warning.y = None

        def do_move(event):
            deltax = event.x - custom_warning.x
            deltay = event.y - custom_warning.y
            x = custom_warning.winfo_x() + deltax
            y = custom_warning.winfo_y() + deltay
            custom_warning.geometry(f"+{x}+{y}")

        title_bar.bind('<Button-1>', start_move)
        title_bar.bind('<ButtonRelease-1>', stop_move)
        title_bar.bind('<B1-Motion>', do_move)
        title_text.bind('<Button-1>', start_move)
        title_text.bind('<ButtonRelease-1>', stop_move)
        title_text.bind('<B1-Motion>', do_move)
        
        # 날짜 라벨
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        date_label = tk.Label(main_container,
                            text=f"{current_date} {current_korean_weekday}",
                            font=("맑은 고딕", 16),
                            bg='white',
                            fg='#666666')
        date_label.pack(pady=(30, 0), anchor='center')
        
        # 제목 라벨
        title_label = tk.Label(main_container, 
                             text="오늘의 식단",
                             font=("맑은 고딕", 32, "bold"),
                             bg='white',
                             fg='#006F3F')
        title_label.pack(anchor='center')
        
        # 구분선
        separator = tk.Frame(main_container, height=1, bg='#e0e0e0')
        separator.pack(fill='x', padx=0, pady=(20, 0))
        
        # 스크롤 영역을 포함할 중간 프레임
        scroll_container = tk.Frame(main_container, bg='white')
        scroll_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # 스크롤바를 포함할 캔버스 생성
        canvas = tk.Canvas(scroll_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        
        # 스크롤될 내용을 포함할 프레임
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        # 스크롤바 설정
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # 캔버스에 프레임 추가
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=window_width-60)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 캔버스와 스크롤바 배치
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def create_meal_frame(parent, title, menu_text):
            frame = tk.Frame(parent, bg='white')
            frame.pack(fill='x', pady=12)
            
            title_container = tk.Frame(frame, bg='white')
            title_container.pack(fill='x', padx=20)
            
            meal_title = tk.Label(title_container, 
                                text=title,
                                font=("맑은 고딕", 18, "bold"),
                                bg='white',
                                fg='#006F3F')
            meal_title.pack(pady=(8, 8), anchor='center')  # 중앙 정렬 유지
            
            separator = tk.Frame(frame, height=2, bg='#e0e0e0')
            separator.pack(fill='x', padx=20)
            
            menu_label = tk.Label(frame,
                                text=menu_text,
                                font=("맑은 고딕", 16),
                                bg='white',
                                fg='#333333',
                                wraplength=600,
                                justify='center')  # 중앙 정렬 유지
            menu_label.pack(pady=(12, 8), padx=20)
        
        # 각 식사 프레임 생성
        create_meal_frame(scrollable_frame, "🌅아침", today_menu['breakfast'])
        create_meal_frame(scrollable_frame, "☀점심 A", today_menu['lunch A'])
        create_meal_frame(scrollable_frame, "☀점심 B", today_menu['lunch B'])
        create_meal_frame(scrollable_frame, "🌙저녁", today_menu['dinner'])
        
        # 버튼 프레임
        button_frame = tk.Frame(main_container, bg='white')
        button_frame.pack(fill='x', pady=20)
        
        # 확인 버튼
        close_button = tk.Button(button_frame,
                               text="닫기",
                               command=lambda: on_closing(),
                               font=("맑은 고딕", 16),
                               bg='#006F3F',
                               fg='white',
                               width=10,
                               relief='flat',
                               cursor='hand2')
        close_button.pack(pady=15)
        
        # 창이 닫힐 때 프로그램 종료
        def on_closing():
            custom_warning.destroy()
            root.destroy()
            sys.exit()
            
        custom_warning.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 버튼 호버 효과
        def on_enter(e):
            close_button['bg'] = '#005732'  # 호버시 약간 더 어두운 녹색
        
        def on_leave(e):
            close_button['bg'] = '#006F3F'  # 원래 전남대 로고 초록색으로
            
        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

        custom_warning.mainloop()

    # 현재 요일의 메뉴 가져오기
    today_menu = weekly_menu[current_korean_weekday]
    
    # GUI 표시
    show_custom_warning("")

else:
    print("페이지를 불러올 수 없습니다. 상태 코드:", response.status_code)
