import pygame
from random import *


# 레벨에 맞게 설정
def setup(level) :
    # 얼마동안 숫자를 보여줄 것인가?
    global display_time
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1)
    
    # 얼마나 많은 숫자를 보여줄 것인가?
    number_count = (level // 3) + 5
    number_count = min (number_count, 20)  # 최대 20 으로 제한

# 실제 화면에 grid 형태로 숫자를 랜덤으로 배치
    shuffle_grid(number_count) 

# 숫자 섞기 (이 프로젝트에서 매우 중요)
def shuffle_grid(number_count) :
    rows = 5
    columns = 9

    cell_size = 130  # 각 grid cell 별 가로, 세로 크기
    button_size = 110  # grid cell 내 실제로 그려질 버튼 크기
    screen_left_margin = 55  # 전체 스크린 왼쪽 여백
    screen_top_margin = 20  # 전체 스크린 상단 여백

    # [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    grid = [[0 for col in range(columns)] for row in range(rows)]  # 5 X 9

    number = 1 # 시작 숫자 1부터 number_count까지 숫자를 배치
    while number <= number_count :
        row_idx = randrange(0, rows)  # 0 ~ 4 중에서 랜덤으로 뽑기
        col_idx = randrange(0, columns) # 0 ~ 8 중에서 랜덤으로 뽑기

        if grid[row_idx][col_idx] == 0 :
            grid[row_idx][col_idx] = number
            number += 1
    
    # 현재 grid cell 위치 기준으로 x, y 위치를 구함            
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)
            
    # 숫자 버튼 그리기    
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)
        


    # 배치된 랜덤 숫자 확인
    # print(grid)


#############################

# 시작 화면 보여주기 
def display_start_screen() :
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)
    # 흰색으로 동그라미를 그리는데, 중심좌표는 start_button 의 중심좌표를 따라가고
    # 반지름은 60, 선 두께는 5

    msg = game_font.render(f'Level{curr_level}', True, WHITE)
    msg_rect = msg.get_rect(center = start_button.center)
    screen.blit(msg, msg_rect)


# 게임 화면 보여주기
def display_game_screen() :
    global hidden 

    if not hidden :
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # ms
        if elapsed_time > display_time : 
            hidden = True

    for idx, rect in enumerate(number_buttons, start = 1) :
        if hidden:  # 숨김 처리
            # 버튼 사각형 그리기    
             pygame.draw.rect(screen, GRAY, rect)
        else : 
            # 실제 숫자 텍스트 입력
            cell_text = game_font.render(str(idx), True, WHITE)
            # 사각상자의 센터값을 가져와서 텍스트를 입력하는 위치의 센터값으로 설정
            text_rect = cell_text.get_rect(center = rect.center)
            
            screen.blit(cell_text, text_rect)


def check_buttons(pos) :
    global start, start_ticks # 전역변수라고 선언     
    
    if start : # 게임이 시작했으면?
        check_number_buttons(pos)    
    elif start_button.collidepoint(pos) : 
        start = True
        start_ticks = pygame.time.get_ticks()  # 타이머 시작(현재시각 저장)
    # pos 에 해당하는 버튼 확인





def check_number_buttons(pos) : 
    global start, hidden, curr_level 

    for button in number_buttons :
        if button.collidepoint(pos) : 
            if button == number_buttons[0] : # 올바른 숫자 클릭
                del number_buttons[0]
                if not hidden :
                    hidden = True  # 숫자 숨김 처리


            else : # 잘못된 숫자 클릭
                game_over()
            break


    # 모든 숫자를 다 맞췄으면, 
    if len(number_buttons) == 0 :
        start = False
        hidden = False
        curr_level += 1 
        setup(curr_level)

# 게임 종료 처리, 메시지도 보여줌
def game_over() :
    global running
    running = False

    msg = game_font.render(f'{curr_level}', True, WHITE)
    msg_rect = msg.get_rect(center = (screen_width / 2, screen_height / 2))

    screen.fill(BLACK)  # 숫자들과 겹쳐 보이지 않도록 먼저 검은 화면 표시
    screen.blit(msg, msg_rect)



# 기본 초기화(반드시 필요)
pygame.init() 

# 화면 크기 설정
screen_width = 1280 # 가로크기
screen_height = 720 # 세로크기
screen = pygame.display.set_mode((screen_width, screen_height)) # tuple 형태로 입력

# 화면 타이틀 설정
pygame.display.set_caption('게임 만들기2-memory game')  # 게임 이름

# 게임 폰트 정의
game_font = pygame.font.Font(None, 120)

# 시작 버튼
start_button = pygame.Rect(0, 0 , 120, 120)
start_button.center = (120, screen_height - 120)

# 색깔
BLACK = (0, 0, 0)  # RGB
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# 플레이어가 눌려야 하는 버튼을 관리하는 리스트
number_buttons = []


curr_level = 1  # 현재 레벨 

# 숫자를 보여주는 시간
display_time = None 

# 시간 계산 (현재 시간 정보를 저장)
start_ticks = None

# 게임 시작 전에 게임 설정 함수 수행
setup(curr_level)

# 게임 시작 여부
start = False

# 숫자 숨김 여부 (사용자가 1을 클릭했거나, 보여주는 시간 초과되었을 때)
hidden = False

# 1. 게임 루프
running = True  # 게임이 진행 중인가

while running :
    click_pos = None

# 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get() :  # 어떤 이벤트가 발생했는가?
        if event.type == pygame.QUIT : # 창이 닫히는 이벤트가 발생했는가?
            running = False  # 게임이 진행중이 아님
        elif event.type == pygame.MOUSEBUTTONUP : # 사용자가 마우스를 클릭했을때
            click_pos = pygame.mouse.get_pos()
            # print(click_pos)



# 화면 전체를 검정으로 색칠
    screen.fill(BLACK)

    if start: 
        display_game_screen() # 게임 화면 표시
    else : 
        display_start_screen() # 시작 화면 표시

# 사용자가 클릭한 좌표값이 있다면 (어딘가 클릭했다면)
    if click_pos :
        check_buttons(click_pos)



# 화면 업데이트
    pygame.display.update()

# 5초 정도 레벨 보여줌
pygame.time.delay(5000)

# pygame 종료
pygame.quit()
 