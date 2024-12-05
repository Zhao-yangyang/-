# Python 俄罗斯方块游戏

这是一个使用 Python 和 Pygame 库开发的经典俄罗斯方块游戏。

## 运行要求

- Python 3.6 或更高版本
- pygame
- pyinstaller (仅打包时需要)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 直接运行

```bash
python tetris.py
```

## 打包应用

```bash
python build.py
```

打包完成后，可执行文件会在 `dist/macOS` 目录中。

## 游戏操作

- ←/→ 键：左右移动方块
- ↓ 键：加速下落
- ↑ 键：旋转方块
- 空格键：直接落到底部
- ESC 键：暂停游戏
- Q 键：退出游戏

## 游戏规则

1. 方块会从屏幕顶部落下
2. 使用方向键移动和旋转方块
3. 当一行被完全填满时，该行会消除并获得分数
4. 游戏会随着分数提升而加快速度
5. 当方块堆到屏幕顶部时游戏结束