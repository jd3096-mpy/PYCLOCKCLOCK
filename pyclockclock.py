import pygame
import math
import random
import time
from pygame.locals import *
from pygame import gfxdraw
from moviepy import *

pygame.init()

clock_color = [2,2,2] 
width, height = 1280, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("同步矩阵时钟")
clock = pygame.time.Clock()

# 加载背景视频
try:
    video = VideoFileClip("bg.mp4")
    video_frame = video.get_frame(0)
    video_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))
except:
    pass

cols, rows = 12, 3
clock_count = cols * rows
hand_length = 45
hand_width = 5

animation_duration = 0.8
current_angles = [[0, 0, 0] for _ in range(clock_count)]
start_angles = [[0, 0, 0] for _ in range(clock_count)]
target_angles = [[0, 0, 0] for _ in range(clock_count)]
deltas = [[0, 0, 0] for _ in range(clock_count)]
current_alpha = [[255 for _ in range(3)] for _ in range(clock_count)]  # 新增透明度数组
start_alpha = [[255 for _ in range(3)] for _ in range(clock_count)]
target_alpha = [[255 for _ in range(3)] for _ in range(clock_count)]
delta_alpha = [[0 for _ in range(3)] for _ in range(clock_count)]
animation_start = 0
is_animating = False
run_clock = True

num_map = [
    [0, 1, 12, 13, 24, 25],
    [2, 3, 14, 15, 26, 27],
    [4, 5, 16, 17, 28, 29],
    [6, 7, 18, 19, 30, 31],
    [8, 9, 20, 21, 32, 33],
    [10, 11, 22, 23, 34, 35],
]
char_map = {
    "1": [
        [-1, -1, -1],
        [180, -1, -1],
        [-1, -1, -1],
        [180, 0, -1],
        [-1, -1, -1],
        [0, -1, -1],
    ],
    "2": [
        [90, -1, -1],
        [270, 180, -1],
        [180, 90, -1],
        [270, 0, -1],
        [90, 0, -1],
        [270, -1, -1],
    ],
    "3": [
        [90, -1, -1],
        [270, 180, -1],
        [90, -1, -1],
        [270, 180, 0],
        [90, -1, -1],
        [270, 0, -1],
    ],
    "4": [
        [180, -1, -1],
        [180, -1, -1],
        [90, 0, -1],
        [270, 180, 0],
        [-1, -1, -1],
        [0, -1, -1],
    ],
    "5": [
        [180, 90, -1],
        [270, -1, -1],
        [90, 0, -1],
        [270, 180, -1],
        [90, -1, -1],
        [270, 0, -1],
    ],
    "6": [
        [180, 90, -1],
        [270, -1, -1],
        [180, 90, 0],
        [270, 180, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "7": [
        [90, -1, -1],
        [270, 180, -1],
        [-1, -1, -1],
        [180, 0, -1],
        [-1, -1, -1],
        [0, -1, -1],
    ],
    "8": [
        [180, 90, -1],
        [270, 180, -1],
        [180, 90, 0],
        [270, 180, 0],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "9": [
        [180, 90, -1],
        [270, 180, -1],
        [90, 0, -1],
        [270, 180, 0],
        [90, -1, -1],
        [270, 0, -1],
    ],
    "0": [
        [180, 90, -1],
        [270, 180, -1],
        [180, 0, -1],
        [180, 0, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "A": [
        [0, -1, -1],
        [90, -1, -1],
        [90, -1, -1],
        [0, -1, -1],
        [90, 0, -1],
        [-1, -1, -1],
    ],
    "B": [
        [0, -1, -1],
        [90, 0, 180],
        [180, -1, -1],
        [0, -1, -1],
        [90, 0, -1],
        [270, -1, -1],
    ],  #
    "C": [
        [180, 90, -1],
        [270, -1, -1],
        [180, 0, -1],
        [-1, -1, -1],
        [90, 0, -1],
        [270, -1, -1],
    ],  #
    "D": [
        [180, 125, -1],
        [-1, -1, -1],
        [180, 0, -1],
        [180, 0, -1],
        [55, 0, -1],
        [-1, -1, -1],
    ],  #
    "E": [
        [0, -1, -1],
        [270, -1, -1],
        [180, -1, -1],
        [0, -1, -1],
        [90, 0, -1],
        [270, -1, -1],
    ],
    "F": [
        [0, -1, -1],
        [270, -1, -1],
        [-1, -1, -1],
        [0, -1, -1],
        [90, -1, -1],
        [-1, -1, -1],
    ],
    "G": [
        [0, -1, -1],
        [270, 180, -1],
        [180, 0, -1],
        [0, -1, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "H": [
        [-1, -1, -1],
        [90, 270, -1],
        [-1, -1, -1],
        [0, -1, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "I": [
        [0, -1, -1],
        [270, -1, -1],
        [180, -1, -1],
        [0, -1, -1],
        [-1, -1, -1],
        [270, -1, -1],
    ],
    "J": [
        [-1, -1, -1],
        [270, 180, -1],
        [-1, -1, -1],
        [180, 0, -1],
        [315, 90, -1],
        [270, 0, -1],
    ],  #
    "K": [
        [180, -1, -1],
        [225, -1, -1],
        [135, 45, -1],
        [-1, -1, -1],
        [0, -1, -1],
        [315, -1, -1],
    ],  #
    "L": [
        [180, -1, -1],
        [-1, -1, -1],
        [180, 0, -1],
        [-1, -1, -1],
        [90, 0, -1],
        [270, -1, -1],
    ],  #
    "M": [
        [90, -1, -1],
        [270, 180, 90],
        [90, 270, -1],
        [180, 0, -1],
        [-1, -1, -1],
        [0, -1, -1],
    ],
    "N": [
        [90, -1, -1],
        [270, 180, -1],
        [90, 270, -1],
        [180, 0, -1],
        [-1, -1, -1],
        [0, -1, -1],
    ],
    "O": [
        [180, 90, -1],
        [270, 180, -1],
        [180, 0, -1],
        [180, 0, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],  #
    "P": [
        [0, -1, -1],
        [90, 270, -1],
        [180, 90, -1],
        [0, -1, -1],
        [90, -1, -1],
        [-1, -1, -1],
    ],
    "Q": [
        [180, 90, -1],
        [270, 180, 0],
        [180, 0, -1],
        [180, 0, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "R": [
        [0, -1, -1],
        [90, 270, -1],
        [180, 90, 0],
        [0, -1, -1],
        [90, -1, -1],
        [270, -1, -1],
    ],
    "S": [
        [180, 90, -1],
        [270, -1, -1],
        [90, 0, -1],
        [270, 180, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "T": [
        [0, -1, -1],
        [270, -1, -1],
        [-1, -1, -1],
        [0, -1, -1],
        [90, -1, -1],
        [-1, -1, -1],
    ],
    "U": [
        [-1, -1, -1],
        [270, 180, -1],
        [180, 0, -1],
        [0, -1, -1],
        [90, 0, -1],
        [270, -1, -1],
    ],
    "V": [
        [90, -1, -1],
        [270, 180, -1],
        [180, 0, -1],
        [0, -1, -1],
        [-1, -1, -1],
        [270, -1, -1],
    ],
    "W": [
        [90, 270, -1],
        [270, 180, 90],
        [180, 0, 270],
        [0, -1, -1],
        [-1, -1, -1],
        [270, -1, -1],
    ],
    "X": [
        [90, 270, -1],
        [270, 180, 90],
        [180, 90, 270],
        [0, 270, -1],
        [90, 0, -1],
        [270, 0, -1],
    ],
    "Y": [
        [90, 270, -1],
        [270, 180, 0],
        [-1, -1, -1],
        [0, -1, -1],
        [90, -1, -1],
        [270, -1, -1],
    ],
    "Z": [
        [90, -1, -1],
        [270, 180, -1],
        [180, 90, -1],
        [270, 0, -1],
        [90, 0, -1],
        [270, -1, -1],
    ],
    " ": [
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1],
        [-1, -1, -1],
    ],
}

try:
    background = pygame.image.load("bg.jpg")
    background = pygame.transform.smoothscale(background, (width, height))
except:
    background = pygame.Surface((width, height))
    background.fill(WHITE)


def calculate_hand_points(center, angle):
    angle_rad = math.radians(angle - 90)
    main_vec = (math.cos(angle_rad) * hand_length, math.sin(angle_rad) * hand_length)
    perp_rad = angle_rad + math.pi / 2
    perp_vec = (
        math.cos(perp_rad) * hand_width / 2,
        math.sin(perp_rad) * hand_width / 2,
    )

    return [
        (center[0] - perp_vec[0], center[1] - perp_vec[1]),
        (center[0] + main_vec[0] - perp_vec[0], center[1] + main_vec[1] - perp_vec[1]),
        (center[0] + main_vec[0] + perp_vec[0], center[1] + main_vec[1] + perp_vec[1]),
        (center[0] + perp_vec[0], center[1] + perp_vec[1]),
    ]


def draw_aa_hand(surface, center, angle, alpha):
    global clock_color
    if angle == -1 or alpha <= 0:
        return  # 透明度为0或角度无效时不绘制
    points = calculate_hand_points(center, angle)
    color = (clock_color[0], clock_color[1], clock_color[2], int(alpha))  # 使用带透明度的颜色
    gfxdraw.aapolygon(surface, points, color)
    gfxdraw.filled_polygon(surface, points, color)


def calculate_positions():
    horizontal_spacing = 8
    vertical_spacing = 8

    max_clock_width = (width - (cols - 1) * horizontal_spacing) // cols
    max_clock_height = (height - (rows - 1) * vertical_spacing) // rows
    clock_size = min(max_clock_width, max_clock_height)

    total_width = cols * clock_size + (cols - 1) * horizontal_spacing
    total_height = rows * clock_size + (rows - 1) * vertical_spacing

    start_x = (width - total_width) // 2
    start_y = (height - total_height) // 2

    return [
        (
            int(start_x + col * (clock_size + horizontal_spacing) + clock_size // 2),
            int(start_y + row * (clock_size + vertical_spacing) + clock_size // 2),
        )
        for row in range(rows)
        for col in range(cols)
    ]


clock_positions = calculate_positions()


def show_char(content):
    global start_angles, target_angles, deltas, animation_start, is_animating
    global start_alpha, target_alpha, delta_alpha

    for idx in range(clock_count):
        start_angles[idx] = current_angles[idx][:]

    i = 0
    for c in content:
        for j in range(6):
            target_angles[num_map[i][j]] = char_map[c][j]
        i += 1

    # 设置透明度动画参数
    for idx in range(clock_count):
        for hand in range(3):
            target = target_angles[idx][hand]
            target_alpha[idx][hand] = 255 if target != -1 else 0

    start_alpha = [row[:] for row in current_alpha]
    for idx in range(clock_count):
        for hand in range(3):
            delta_alpha[idx][hand] = target_alpha[idx][hand] - start_alpha[idx][hand]
            # 计算角度变化量（特殊处理-1的情况）
            if target_angles[idx][hand] == -1:
                deltas[idx][hand] = 0  # 角度不变化
            else:
                start = start_angles[idx][hand]
                target = target_angles[idx][hand]
                deltas[idx][hand] = (target - start) % 360

    animation_start = pygame.time.get_ticks()
    is_animating = True


def update_angles():
    global current_angles, current_alpha, is_animating
    if not is_animating:
        return

    elapsed = (pygame.time.get_ticks() - animation_start) / 1000
    if elapsed >= animation_duration:
        # 动画结束时设置最终状态
        for idx in range(clock_count):
            for hand in range(3):
                current_angles[idx][hand] = (
                    target_angles[idx][hand] if target_angles[idx][hand] != -1 else -1
                )
                current_alpha[idx][hand] = target_alpha[idx][hand]
        is_animating = False
    else:
        progress = elapsed / animation_duration
        for idx in range(clock_count):
            for hand in range(3):
                # 更新角度（特殊处理目标为-1的情况）
                if target_angles[idx][hand] == -1:
                    current_angles[idx][hand] = start_angles[idx][
                        hand
                    ]  # 保持原角度直到动画结束
                else:
                    current_angles[idx][hand] = (
                        start_angles[idx][hand] + deltas[idx][hand] * progress
                    ) % 360

                # 更新透明度
                current_alpha[idx][hand] = (
                    start_alpha[idx][hand] + delta_alpha[idx][hand] * progress
                )
                current_alpha[idx][hand] = max(0, min(255, current_alpha[idx][hand]))


def create_mask_surface():
    """创建遮罩层，只显示表盘圆形的部分"""
    mask_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    mask_surface.fill((255, 255, 255, 255))  # 填充黑色

    # 计算时钟的半径
    clock_size = min(
        (width - (cols - 1) * 8) // cols, (height - (rows - 1) * 8) // rows
    )
    clock_radius = clock_size // 2

    # 在每个时钟位置挖出圆形区域
    for pos in clock_positions:
        pygame.draw.circle(mask_surface, (0, 0, 0, 0), pos, clock_radius)

    return mask_surface


def get_current_time():
    """获取当前时间并格式化为字符串"""
    current_time = time.strftime("%H%M%S")
    return current_time


mask_surface = create_mask_surface()

running = True
last_time_update = 0
video_start_time = pygame.time.get_ticks()
show_initial_text = True
initial_start_time = pygame.time.get_ticks()

show_char("JD3096")
while running:
    current_time = pygame.time.get_ticks()
    
    # 事件处理部分
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif not show_initial_text:  # 只在非初始阶段处理按键事件
            if event.type == KEYDOWN:
                if event.key == K_1:
                    run_clock = True
                elif event.key == K_2:
                    run_clock = False
                    date = time.strftime("%y%m%d")
                    show_char(date)

    update_angles()

    if show_initial_text:
        if current_time - initial_start_time >= 2000:
            show_initial_text = False
            last_time_update = current_time  
            run_clock = True  
    else:
        if run_clock:
            if current_time - last_time_update >= 1000: 
                time_str = get_current_time()
                show_char(time_str)
                last_time_update = current_time
                
#     video_time = (current_time - video_start_time) / 1000  # 转换为秒
#     if video_time > video.duration:
#         video_start_time = current_time
#         video_time = 0
#     video_frame = video.get_frame(video_time)
#     video_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))
# 
#     # 绘制背景视频
#     screen.blit(video_surface, (0, 0))

    screen.blit(background, (0, 0))
    hand_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    hand_surface.fill((0, 0, 0, 0))

    for idx, pos in enumerate(clock_positions):
        for hand in range(3):
            draw_aa_hand(
                hand_surface, pos, current_angles[idx][hand], current_alpha[idx][hand]
            )
        gfxdraw.filled_circle(hand_surface, pos[0], pos[1], 6, (clock_color[0], clock_color[1], clock_color[2], 255))

    screen.blit(hand_surface, (0,0))
    screen.blit(mask_surface, (0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()