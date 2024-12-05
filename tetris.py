# -*- coding: utf-8 -*-

import pygame
import sys
import os
import math
from game.colors import BLACK, WHITE, GRAY, BACKGROUND, LIGHT_BG, TEXT_PRIMARY, TEXT_SECONDARY, NEUTRAL
from game.block import Block
from game.board import Board
from game.button import Button
from game.ui_constants import *

# 初始化 Pygame
pygame.init()

# 游戏常量
BLOCK_SIZE = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# 计算游戏板的位置使其居中
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_WIDTH * BLOCK_SIZE) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - BOARD_HEIGHT * BLOCK_SIZE) // 2

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TETRIS')

# 设置中文字体
def get_font(size):
    # macOS 系统常用中文字体
    system_fonts = [
        'PingFang SC',        # 苹方
        'STHeiti',            # 华文黑体
        'Heiti TC',           # 黑体-繁
        'Hiragino Sans GB',   # 冬青黑体
        'Apple LiGothic',     # 苹果丽黑
    ]
    
    # 获取系统可用字体列表
    available_fonts = pygame.font.get_fonts()
    print(f"系统可用字体: {available_fonts}")
    
    # 尝试加载系统字体
    for font_name in system_fonts:
        try:
            # 转换字体名称为小写并去除空格，以匹系统字体列表格式
            font_key = font_name.lower().replace(' ', '')
            if font_key in available_fonts:
                font = pygame.font.SysFont(font_name, size)
                # 测试字体是否能渲染中文
                test_surface = font.render('测试', True, (255, 255, 255))
                print(f"成功加载字体: {font_name}")
                return font
        except Exception as e:
            print(f"加载字体 {font_name} 失败: {str(e)}")
            continue
    
    # 如果系统字体都失败了，尝试从固定路径加载字体
    mac_font_paths = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/Library/Fonts/Arial Unicode.ttf'
    ]
    
    for font_path in mac_font_paths:
        try:
            if os.path.exists(font_path):
                font = pygame.font.Font(font_path, size)
                test_surface = font.render('测试', True, (255, 255, 255))
                print(f"成功加载字体文件: {font_path}")
                return font
        except Exception as e:
            print(f"加载字体文件 {font_path} 失败: {str(e)}")
            continue
    
    print("警告: 无法载中文字体，将使用系统默认字体")
    return pygame.font.Font(None, size)

# 创建字体对
font = get_font(36)
title_font = get_font(72)
rule_font = get_font(28)

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

def _lerp_color(start_color, end_color, amount):
    """颜色渐变插值函数"""
    return tuple(int(start + (end - start) * amount) 
                for start, end in zip(start_color, end_color))

def draw_menu(screen, buttons):
    # 绘制渐变背景
    for i in range(SCREEN_HEIGHT):
        # 计算当前位置的渐变颜色
        amount = i / SCREEN_HEIGHT
        color = _lerp_color(BACKGROUND, LIGHT_BG, amount)
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))
    
    try:
        # 绘制标题
        title_text = title_font.render(GAME_TITLE, True, TEXT_PRIMARY)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, TITLE_Y))
        
        # 添加标题阴影效果
        shadow_surface = title_font.render(GAME_TITLE, True, NEUTRAL)
        shadow_rect = title_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(title_text, title_rect)

        # 绘制游戏规则
        for i, rule in enumerate(GAME_RULES):
            rule_text = rule_font.render(rule, True, TEXT_SECONDARY)
            rule_rect = rule_text.get_rect(left=RULES_LEFT_MARGIN, 
                                         top=RULES_START_Y + i * RULES_LINE_HEIGHT)
            screen.blit(rule_text, rule_rect)
    except Exception as e:
        print(f"渲染文字时出错: {str(e)}")

    # 绘制按钮
    for button in buttons:
        button.draw(screen)

def draw_game_board(screen, board, current_block, next_block, game_state):
    # 绘制毛玻璃效果的背景
    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_surface.fill(BACKGROUND)
    bg_surface.set_alpha(230)
    screen.blit(bg_surface, (0, 0))

    # 绘制游戏区域背景
    board_bg_rect = pygame.Rect(BOARD_OFFSET_X - 10, BOARD_OFFSET_Y - 10,
                               BOARD_WIDTH * BLOCK_SIZE + 20,
                               BOARD_HEIGHT * BLOCK_SIZE + 20)
    pygame.draw.rect(screen, LIGHT_BG, board_bg_rect, border_radius=15)
    pygame.draw.rect(screen, NEUTRAL, board_bg_rect, 1, border_radius=15)

    # 绘制网格线
    for x in range(BOARD_WIDTH + 1):
        pygame.draw.line(screen, NEUTRAL,
                        (BOARD_OFFSET_X + x * BLOCK_SIZE, BOARD_OFFSET_Y),
                        (BOARD_OFFSET_X + x * BLOCK_SIZE, BOARD_OFFSET_Y + BOARD_HEIGHT * BLOCK_SIZE))
    for y in range(BOARD_HEIGHT + 1):
        pygame.draw.line(screen, NEUTRAL,
                        (BOARD_OFFSET_X, BOARD_OFFSET_Y + y * BLOCK_SIZE),
                        (BOARD_OFFSET_X + BOARD_WIDTH * BLOCK_SIZE, BOARD_OFFSET_Y + y * BLOCK_SIZE))

    # ... (其余绘制代码保持不变)

def main():
    # 创建游戏实例
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    current_block = Block()
    next_block = Block()
    clock = pygame.time.Clock()
    
    # 创建按钮
    center_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    
    # 主菜单按钮
    start_button = Button(center_x, MENU_BUTTON_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 
                         "新游戏", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    continue_button = Button(center_x, MENU_BUTTON_START_Y + MENU_BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT, 
                         "继续游戏", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    quit_button = Button(center_x, MENU_BUTTON_START_Y + MENU_BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT,
                        QUIT_BUTTON_TEXT, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    
    # 游戏界面的按钮
    pause_button = Button(SCREEN_WIDTH - 140, 20, 120, 40, 
                         PAUSE_BUTTON_TEXT, BUTTON_COLOR, BUTTON_HOVER_COLOR, 24)
    
    # 暂停菜单按钮
    resume_button = Button(center_x, MENU_BUTTON_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT,
                          RESUME_BUTTON_TEXT, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    restart_button = Button(center_x, MENU_BUTTON_START_Y + MENU_BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT,
                          "重新开始", BUTTON_COLOR, BUTTON_HOVER_COLOR)
    back_to_menu_button = Button(center_x, MENU_BUTTON_START_Y + MENU_BUTTON_GAP * 2, BUTTON_WIDTH, BUTTON_HEIGHT,
                          "返回主菜单", BUTTON_COLOR, BUTTON_HOVER_COLOR)

    # 游戏状态
    game_state = GameState.MENU
    fall_time = 0
    fall_speed = 0.5
    # 保存上一次的游戏状，用于继续游戏
    saved_game_state = None

    # 游戏主循环
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            # 添加对键盘事件的处理
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    break
                elif event.key == pygame.K_ESCAPE and game_state == GameState.PLAYING:
                    game_state = GameState.PAUSED
                    saved_game_state = (board, current_block, next_block)
                
                # 游戏进行时的按键控制
                if game_state == GameState.PLAYING:
                    if event.key == pygame.K_LEFT:
                        current_block.x -= 1
                        if not board.is_valid_move(current_block):
                            current_block.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_block.x += 1
                        if not board.is_valid_move(current_block):
                            current_block.x -= 1
                    elif event.key == pygame.K_UP:
                        # 尝试旋转，如果不合法就恢复
                        current_block.rotate()
                        if not board.is_valid_move(current_block):
                            current_block.rotate_back()
                    elif event.key == pygame.K_DOWN:
                        fall_speed = 0.1
                    elif event.key == pygame.K_SPACE:
                        # 硬降落
                        while board.is_valid_move(current_block):
                            current_block.y += 1
                        current_block.y -= 1
                        board.lock_block(current_block)
                        current_block = next_block
                        next_block = Block()
                        fall_time = 0
                        fall_speed = 0.5

            # 处理按键松开事件
            elif event.type == pygame.KEYUP:
                if game_state == GameState.PLAYING:
                    if event.key == pygame.K_DOWN:
                        fall_speed = 0.5

            # 处理按钮事件
            if game_state == GameState.MENU:
                # 更新所有按钮的状态
                for button in [start_button, continue_button, quit_button]:
                    if button.handle_event(event):
                        if button == start_button:
                            game_state = GameState.PLAYING
                            board = Board(BOARD_WIDTH, BOARD_HEIGHT)
                            current_block = Block()
                            next_block = Block()
                        elif button == continue_button and saved_game_state:
                            board, current_block, next_block = saved_game_state
                            game_state = GameState.PAUSED
                        elif button == quit_button:
                            running = False
                            break

            elif game_state == GameState.PAUSED:
                if resume_button.handle_event(event):
                    game_state = GameState.PLAYING
                elif restart_button.handle_event(event):
                    game_state = GameState.PLAYING
                    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
                    current_block = Block()
                    next_block = Block()
                elif back_to_menu_button.handle_event(event):
                    game_state = GameState.MENU
                    saved_game_state = (board, current_block, next_block)
            elif game_state == GameState.GAME_OVER:
                if restart_button.handle_event(event):
                    game_state = GameState.PLAYING
                    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
                    current_block = Block()
                    next_block = Block()
                elif back_to_menu_button.handle_event(event):
                    game_state = GameState.MENU
                    saved_game_state = None
            elif game_state == GameState.PLAYING:
                if pause_button.handle_event(event):
                    game_state = GameState.PAUSED
                    saved_game_state = (board, current_block, next_block)

        # 更新游戏态
        if game_state == GameState.PLAYING:
            fall_time += dt
            if fall_time >= fall_speed:
                current_block.y += 1
                if not board.is_valid_move(current_block):
                    current_block.y -= 1
                    board.lock_block(current_block)
                    current_block = next_block
                    next_block = Block()
                    if not board.is_valid_move(current_block):
                        game_state = GameState.GAME_OVER
                fall_time = 0
                fall_speed = 0.5

        # 绘制游戏画
        screen.fill(BLACK)

        if game_state == GameState.MENU:
            if saved_game_state:
                # 有存档时显示三个按钮
                buttons = [start_button, continue_button, quit_button]
                # 更新退出按钮位置到第三行
                quit_button.rect.y = MENU_BUTTON_START_Y + MENU_BUTTON_GAP * 2
            else:
                # 无存档时只显示两个按钮
                buttons = [start_button, quit_button]
                # 更新退出按钮位置到第二行
                quit_button.rect.y = MENU_BUTTON_START_Y + MENU_BUTTON_GAP
            
            draw_menu(screen, buttons)
        else:
            # 绘制游戏边框
            pygame.draw.rect(screen, WHITE, 
                           (BOARD_OFFSET_X - 2, BOARD_OFFSET_Y - 2,
                            BOARD_WIDTH * BLOCK_SIZE + 4,
                            BOARD_HEIGHT * BLOCK_SIZE + 4), 2)

            # 绘制游戏板
            for y in range(board.height):
                for x in range(board.width):
                    color = board.board[y][x]
                    pygame.draw.rect(screen, color,
                                   (BOARD_OFFSET_X + x * BLOCK_SIZE,
                                    BOARD_OFFSET_Y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

            # 绘制当前方块
            if game_state == GameState.PLAYING:
                positions = current_block.get_positions()
                for x, y in positions:
                    if y >= 0:
                        pygame.draw.rect(screen, current_block.color,
                                       (BOARD_OFFSET_X + x * BLOCK_SIZE,
                                        BOARD_OFFSET_Y + y * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

            # 绘制分数（移到左上角）
            score_text = font.render(f'{SCORE_TEXT}: {board.score}', True, WHITE)
            score_rect = score_text.get_rect(left=20, top=20)
            screen.blit(score_text, score_rect)

            # 绘制暂停按钮（右上角）
            pause_button.draw(screen)

            # 绘制下一个块预览（保持在右侧）
            next_text = font.render(NEXT_BLOCK_TEXT, True, WHITE)
            screen.blit(next_text, (SCREEN_WIDTH - 150, 80))  # Y坐标改为80
            
            preview_offset_x = SCREEN_WIDTH - 120
            preview_offset_y = 120  # Y坐标改为120
            for y in range(len(next_block.shape)):
                for x in range(len(next_block.shape[y])):
                    if next_block.shape[y][x]:
                        pygame.draw.rect(screen, next_block.color,
                                       (preview_offset_x + x * BLOCK_SIZE,
                                        preview_offset_y + y * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

            # 绘制游戏结或暂停信息
            if game_state == GameState.GAME_OVER:
                game_over_text = font.render(GAME_OVER_TEXT, True, WHITE)
                screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 100))
                restart_button.draw(screen)
                back_to_menu_button.draw(screen)
            elif game_state == GameState.PAUSED:
                pause_text = font.render(PAUSE_BUTTON_TEXT, True, WHITE)
                screen.blit(pause_text, 
                           (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 150))
                resume_button.draw(screen)
                restart_button.draw(screen)
                back_to_menu_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 