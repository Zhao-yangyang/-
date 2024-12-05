import random
from .colors import BLOCK_COLORS

# 定义所有方块形状
SHAPES = [
    [  # I
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
    ],
    [  # J
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],
    ],
    [  # L
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],
    ],
    [  # O
        [[1, 1],
         [1, 1]],
    ],
    [  # S
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],
    ],
    [  # T
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
    ],
    [  # Z
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],
    ]
]

class Block:
    def __init__(self):
        # 随机选择一个方块类型
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx][0]
        self.color = BLOCK_COLORS[self.shape_idx]
        self.rotation = 0
        # 初始位置（居中）
        self.x = 3
        self.y = 0

    def rotate(self):
        """顺时针旋转方块"""
        # 保存旧的形状以便需要时恢复
        self.old_shape = [row[:] for row in self.shape]
        
        # 获取矩阵尺寸
        rows = len(self.shape)
        cols = len(self.shape[0])
        
        # 创建新的旋转后的形状
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        # 执行旋转变换
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]
        
        # 更新形状
        self.shape = rotated
        
        # 保存旧的位置以便需要时恢复
        self.old_x = self.x
        self.old_y = self.y

    def rotate_back(self):
        """恢复到旋转前的状态"""
        if hasattr(self, 'old_shape'):
            self.shape = self.old_shape
            self.x = self.old_x
            self.y = self.old_y

    def get_positions(self):
        """获取方块在游戏板上的所有位置"""
        positions = []
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    positions.append((self.x + x, self.y + y))
        return positions