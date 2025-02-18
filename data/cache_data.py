import pygame
import os

pygame.init()
temp_font_files = []

def get_cache_dir():
    """Trả về đường dẫn thư mục cache, tạo thư mục nếu chưa tồn tại."""
    if os.name == 'nt':  # Windows
        cache_dir = 'C:/.cache_python'
    else:  # Linux và macOS
        cache_dir = os.path.join(os.getenv("HOME"), ".cache_python")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def file_exists(filename):
    return os.path.exists(filename)


def write_to_file(filename, content):
    try:
        with open(filename, 'w') as python_file:
            python_file.write(content)
    except Exception as e:
        print(f"Xảy ra lỗi khi ghi vào {filename}: {e}")

