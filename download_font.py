import os
import urllib.request
import sys

def download_font():
    # 创建fonts目录
    fonts_dir = 'fonts'
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
    
    # 文泉驿微米黑字体下载地址
    font_url = "https://github.com/LayaAir-Demo/font/raw/master/MSYH.TTC"
    font_path = os.path.join(fonts_dir, 'msyh.ttc')
    
    print("开始下载中文字体文件...")
    try:
        urllib.request.urlretrieve(font_url, font_path)
        print(f"字体文件已下载到: {font_path}")
    except Exception as e:
        print(f"下载失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    download_font() 