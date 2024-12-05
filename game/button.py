import pygame
import os
from .colors import (BUTTON_NORMAL, BUTTON_HOVER, BUTTON_ACTIVE, 
                    TEXT_PRIMARY, TEXT_SECONDARY, NEUTRAL)

class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_NORMAL, hover_color=BUTTON_HOVER, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.active_color = BUTTON_ACTIVE
        self.font = self._get_font(font_size)
        self.is_hovered = False
        self.is_pressed = False
        
        # 添加动画相关属性
        self.current_color = list(self.color)  # 转换为列表以支持修改
        self.animation_speed = 5
        self.shadow_offset = 4
        self.corner_radius = 10

    def _get_font(self, size):
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
        
        # 尝试加载系统字体
        for font_name in system_fonts:
            try:
                # 转换字体名称为小写并去除空格，以匹配系统字体列表格式
                font_key = font_name.lower().replace(' ', '')
                if font_key in available_fonts:
                    font = pygame.font.SysFont(font_name, size)
                    # 测试字体是否能渲染中文
                    test_surface = font.render('测试', True, (255, 255, 255))
                    print(f"按钮成功加载字体: {font_name}")
                    return font
            except Exception as e:
                print(f"按钮加载字体 {font_name} 失败: {str(e)}")
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
                    print(f"按钮成功加载字体文件: {font_path}")
                    return font
            except Exception as e:
                print(f"按钮加载字体文件 {font_path} 失败: {str(e)}")
                continue
        
        print("警告: 按钮无法加载中文字体，将使用系统默认字体")
        return pygame.font.Font(None, size)

    def draw(self, screen):
        # 绘制阴影
        shadow_rect = self.rect.copy()
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=self.corner_radius)

        # 动画过渡效果
        target_color = self.hover_color if self.is_hovered else self.color
        if self.is_pressed:
            target_color = self.active_color
        
        # 平滑颜色过渡
        for i in range(3):
            self.current_color[i] = self._lerp(self.current_color[i], target_color[i], self.animation_speed)

        # 绘制按钮背景
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=self.corner_radius)
        
        # 绘制按钮边框
        border_color = TEXT_SECONDARY if self.is_hovered else NEUTRAL
        pygame.draw.rect(screen, border_color, self.rect, 1, border_radius=self.corner_radius)
        
        # 绘制文字
        try:
            text_color = TEXT_PRIMARY if self.is_hovered else TEXT_SECONDARY
            text_surface = self.font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            if self.is_pressed:
                text_rect.y += 1
            screen.blit(text_surface, text_rect)
        except Exception as e:
            print(f"按钮文字渲染失败: {str(e)}")

    def _lerp(self, start, end, amount):
        # 线性插值函数
        return start + (end - start) * amount / 100

    def handle_event(self, event):
        # 获取当前鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                if self.is_hovered:
                    self.is_pressed = True
                    return False  # 不要立即返回True，等待鼠标抬起
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左键释放
                was_pressed = self.is_pressed
                self.is_pressed = False
                # 只有在按钮被按下并且鼠标仍在按钮上时才触发
                if was_pressed and self.is_hovered:
                    return True
        
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            if not self.is_hovered:
                self.is_pressed = False
        
        return False

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value 