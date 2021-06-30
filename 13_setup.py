# 보석을 다양하게 넣어서 게임 완성하기

import pygame
import os
import math

# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)
        
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT  # 집게의 이동 방향
        self.angle_speed = 2.5  # 집게의 각도 변경 폭 (좌우 이동 속도)
        self.angle = 10  # 최초 각도 정의 (오른쪽 끝)


    def update(self, to_x):
        
        if self.direction == LEFT :  # 왼쪽 방향으로 이동하고 있다면
            self.angle += self.angle_speed  # 이동 속도만큼 각도 증가
        elif self.direction == RIGHT :  # 오른쪽 방향으로 이동하고 있다면
            self.angle -= self.angle_speed  # 이동 속도만큼 각도 증가

        # 만약 허용범위 벗어나는 경우 처리
        if self.angle > 170 :
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10 :
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x

        self.rotate()  # 회전 처리

        # print(self.angle, self.direction)

        # rect_center = self.position + self.offset
        # self.rect = self.image.get_rect(center=rect_center)
        
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        # 회전대상이 되는 이미지, 회전 각도, 이미지 크기

        offset_rotated = self.offset.rotate(self.angle)

        self.rect = self.image.get_rect(center = self.position + offset_rotated)

    def set_direction(self, direction):
        self.direction = direction


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3) # 중심점 표시
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # 집게에서 중심점까지 직선 표시

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT



# 보석 클래스
class Gemstone(pygame.sprite.Sprite):  # 상속받아옴
    def __init__(self, image, position, price, speed): 
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self, position, angle):
        r = self.rect.size[0] // 2  
        rad_angle = math.radians(angle)  # 각도
        to_x = r * math.cos(rad_angle)  # 삼각형의 밑변
        to_y = r * math.sin(rad_angle)  # 삼각형의 높이

        self.rect.center = (position[0] + to_x, position[1] + to_y )


def setup_gemstone():
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7


    # 작은 금
    small_gold = Gemstone(gemstone_images[0], (200, 380), small_gold_price, small_gold_speed) # 0번째 이미지를 (200, 380) 위치에 표시
    gemstone_group.add(small_gold)  # 그룹에 추가

    gemstone_group.add(Gemstone(gemstone_images[0], (400, 400), small_gold_price, small_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[0], (600, 450), small_gold_price, small_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[0], (800, 400), small_gold_price, small_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[0], (1150, 380), small_gold_price, small_gold_speed))

    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[1], (800, 500), big_gold_price, big_gold_speed))

    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380), stone_price, stone_speed))
    gemstone_group.add(Gemstone(gemstone_images[2], (700, 330), stone_price, stone_speed))
    gemstone_group.add(Gemstone(gemstone_images[2], (1000, 480), stone_price, stone_speed))

    # 다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420), diamond_price, diamond_speed))
    gemstone_group.add(Gemstone(gemstone_images[3], (150, 500), diamond_price, diamond_speed))


def update_score(score):
    global curr_score
    curr_score += score

def display_time(time):
    txt_timer = game_font.render(f'Time: {time}', True, BLACK)
    screen.blit(txt_timer, (1100, 50))


def display_game_over():
    game_font = pygame.font.SysFont('arialounded', 60) 
    txt_game_over = game_font.render(game_result, True, BLACK)
    rect_game_over = txt_game_over.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
    screen.blit(txt_game_over, rect_game_over)  # 화면 중앙에 표시

def display_score():
    txt_curr_score = game_font.render(f'Curr Score : {curr_score:,}', True, BLACK)
    screen.blit(txt_curr_score, (50, 20))

    txt_goal_score = game_font.render(f'Goal Score : {goal_score:,}', True, BLACK)
    screen.blit(txt_goal_score, (50, 80))



pygame.init()
screen_width = 1200
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Gold Miner')

clock = pygame.time.Clock()
game_font = pygame.font.SysFont('arialrounded', 30)


# 점수 관련 변수
goal_score = 1500
curr_score = 0 

# 게임 오버 관련 변수
game_result = None  # 게임 결과 정의
total_time = 60  # 총 시간

start_ticks = pygame.time.get_ticks()  # 현재 tick을 받아옴


# 게임 관련 변수
default_offset_x_claw = 40  # 중심점으로부터 집게까지의 기본 x 간격

to_x = 0  # x 좌표 기준으로 집게 이미지를 이동시킬 값 저장 변수
caught_gemstone = None  # 집게를 뻗어서 잡은 보석 정보

LEFT = -1  # 왼쪽 방향
RIGHT = 1  # 오른쪽 방향
STOP = 0  # 이동 방향이 고정 (집게를 뻗는 상태)


# 속도 변수
move_speed = 35  # 발사될 때 이동 스피드 (x 좌표 기준으로 증가되는 값)
return_speed = 40  # 아무것도 없이 돌아올때 스피드

# 색깔 변수
RED = (255, 0, 0)
BLACK = (0, 0, 0)


# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)   # 현재 파일의 위치 반환
background = pygame.image.load(os.path.join(current_path, 'background.png'))

# 4개  보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드)

gemstone_images = [
    pygame.image.load(os.path.join(current_path, 'small_gold.png')).convert_alpha(), # 작은 금
    pygame.image.load(os.path.join(current_path, 'big_gold.png')).convert_alpha(),  # 큰 금
    pygame.image.load(os.path.join(current_path, 'stone.png')).convert_alpha(),  # 돌
    pygame.image.load(os.path.join(current_path, 'diamond.png')).convert_alpha()]  # 다이아몬드


# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone()  # 게임에 원하는 만큼의 보석을 정의

# 집게
claw_image = pygame.image.load(os.path.join(current_path, 'claw.png')).convert_alpha()
claw = Claw(claw_image, (screen_width // 2, 110))  # 가로위치는 화면 가로 기준으로 절반, 세로위치는 위에서 110 px


running = True
while running : 

    clock.tick(30)  # FPS 값이 30으로 고정

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN :
            claw.set_direction(STOP)  # 좌우 멈춤
            to_x = move_speed  # move_speed 만큼 쭉 뻗음

    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height :
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw :  # 원위치로 돌아오면
        to_x = 0
        claw.set_init_state()

        if caught_gemstone : # 잡힌 보석이 있으면
            update_score(caught_gemstone.price) # 점수 업데이트
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None

    if not caught_gemstone :  # 잡힌 보석이 없다면 충돌 체크
        for gemstone in gemstone_group :
            # if claw.rect.colliderect(gemstone.rect):  # 직사각형 기준으로 충돌처리
            if pygame.sprite.collide_mask(claw, gemstone):  # 투명영역은 제외하고 실제 이미지 영역의 충돌 처리        
                caught_gemstone = gemstone  # 잡힌 보석
                to_x = -gemstone.speed  # 잡히 보석의 속도에 - 한 값을 이동 속도로 설정
                break

    if caught_gemstone :
        caught_gemstone.set_position(claw.rect.center, claw.angle)      

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen) # 그룹 내 모든 스프라이트를 screen에 그려줘
    claw.update(to_x)
    claw.draw(screen)

    # 점수 정보를 보여줌
    display_score()

    # 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # ms -> s 단위로 변환
    display_time(total_time - int(elapsed_time))  # 남은 시간 표시

    # 남은 시간이 0 이하이면 게임 종료
    if total_time - int(elapsed_time) <= 0 :
        running = False
        if curr_score >= goal_score :
            game_result = 'Mission Complete'
        else:
            game_result = 'Game Over'
        
        # 게임 종료 메시지 표시
        display_game_over()

    pygame.display.update()

pygame.time.delay(2000)  # 2초 대기
pygame.quit() 

# pyinstaller -w(터미널 창 안뜸) 13_setup.py
# DIST 플더가 생성되면 그 안의 13_setup.py 폴더안에 필요한 그림 파일들을 넣어주면 실행됨