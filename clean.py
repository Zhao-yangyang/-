import os
import shutil

def clean_build():
    """清理打包生成的文件"""
    # 需要删除的目录
    dirs_to_remove = [
        'build',                    # PyInstaller构建目录
        'dist',                     # PyInstaller输出目录
        '.buildozer',              # Buildozer构建目录
        '__pycache__',             # Python缓存
        'p4a_hooks',               # Python for Android钩子目录
        'bin',                     # Android构建输出目录
        '.gradle',                 # Gradle缓存目录
        'android',                 # Android项目目录
    ]
    
    # 需要删除的文件
    files_to_remove = [
        '俄罗斯方块.spec',           # PyInstaller规范文件
        '俄罗斯方块.app.spec',       # macOS应用规范文件
        '.buildozer.spec',         # Buildozer配置备份
        'buildozer.spec',          # Buildozer配置文件
        'gradle.properties',       # Gradle配置文件
        'local.properties',        # Android SDK本地配置
        'build.gradle',            # Gradle构建文件
        'settings.gradle',         # Gradle���置文件
        'setup_android.py',        # Android打包配置脚本
        'p4a_patch.py'            # Python for Android补丁脚本
    ]
    
    # 删除目录
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"删除目录: {dir_name}")
            shutil.rmtree(dir_name)
    
    # 删除文件
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            print(f"删除文件: {file_name}")
            os.remove(file_name)
            
    print("清理完成!")

if __name__ == "__main__":
    clean_build() 