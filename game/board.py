from .colors import BLACK

class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[BLACK for _ in range(width)] for _ in range(height)]
        self.score = 0

    def is_valid_move(self, block):
        """检查移动是否有效"""
        positions = block.get_positions()
        for x, y in positions:
            if not (0 <= x < self.width and 0 <= y < self.height):
                return False
            if y >= 0 and self.board[y][x] != BLACK:
                return False
        return True

    def lock_block(self, block):
        """将方块锁定在当前位置"""
        positions = block.get_positions()
        for x, y in positions:
            if y >= 0:
                self.board[y][x] = block.color
        self.clear_lines()

    def clear_lines(self):
        """清除已填满的行并计分"""
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            if all(color != BLACK for color in self.board[y]):
                lines_cleared += 1
                # 将上面的行都下��一行
                for y2 in range(y, 0, -1):
                    self.board[y2] = self.board[y2-1][:]
                # 顶部添加新的空行
                self.board[0] = [BLACK for _ in range(self.width)]
            else:
                y -= 1
        
        # 计算分数（每次消除的行数越多，得分越高）
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800

    def is_game_over(self):
        """检查游戏是否结束"""
        return any(color != BLACK for color in self.board[0]) 