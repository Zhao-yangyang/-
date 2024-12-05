import os
import sys
import shutil
import PyInstaller.__main__

def build_app():
    """打包应用程序"""
    print("开始打包应用...")
    
    # 清理旧的构建文件
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # 获取当前操作系统的分隔符
    separator = ';' if sys.platform == 'win32' else ':'
    
    # 设置打包参数
    args = [
        'tetris.py',  # 主程序文件
        '--name=俄罗斯方块',  # 应用名称
        '--onefile',  # 打包成单个文件
        '--noconsole',  # 不显示控制台窗口
        f'--add-data=game{separator}game',  # 添加game目录，使用正确的分隔符
        '--hidden-import=pygame',  # 添加pygame依赖
        '--hidden-import=game.colors',  # 添加其他必要的模块
        '--hidden-import=game.block',
        '--hidden-import=game.board',
        '--hidden-import=game.button',
        '--hidden-import=game.ui_constants',
        '--collect-all=pygame',  # 收集所有pygame相关文件
        '--clean',  # 清理临时文件
    ]
    
    # 如果存在图标文件，添加图标
    if os.path.exists('assets/icon.ico'):
        args.append('--icon=assets/icon.ico')
    
    try:
        # 在打包之前，确保game目录存在
        if not os.path.exists('game'):
            raise Exception("找不到game目录！")
            
        # 检查必要的模块文件
        required_files = [
            'game/colors.py',
            'game/block.py',
            'game/board.py',
            'game/button.py',
            'game/ui_constants.py',
        ]
        
        for file in required_files:
            if not os.path.exists(file):
                raise Exception(f"找不到必要的文件：{file}")
        
        print("开始执行打包...")
        # 执行打包
        PyInstaller.__main__.run(args)
        print("打包完成！")
        
        # 创建目标目录
        os_name = 'macOS' if sys.platform == 'darwin' else 'Windows'
        target_dir = os.path.join('dist', os_name)
        os.makedirs(target_dir, exist_ok=True)
        
        # 移动打包后的文件到对应目录
        source = os.path.join('dist', '俄罗斯方块')
        if sys.platform == 'win32':
            source += '.exe'
        target = os.path.join(target_dir, os.path.basename(source))
        
        if os.path.exists(source):
            shutil.move(source, target)
            print(f"应用程序已移动到: {target}")
            
            # 添加运行说明
            if sys.platform == 'darwin':
                print("\n在macOS上运行:")
                print(f"1. 打开终端")
                print(f"2. 输入: chmod +x '{target}'")
                print(f"3. 双击运行或在终端中运行: '{target}'")
            else:
                print("\n在Windows上运行:")
                print("直接双击运行生成的exe文件即可")
                
        else:
            print(f"错误：找不到打包后的文件: {source}")
        
    except Exception as e:
        print(f"打包过程中出错: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    build_app() 