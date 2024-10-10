from interface import main_menu
from decryption import *
import os
import sys
import pygame

pygame.init()

# Hàm để lấy đường dẫn tài nguyên khi đóng gói bằng PyInstaller
def resource_path(relative_path):
    """Lấy đường dẫn tới file tài nguyên khi chạy từ file"""
    try:
        base_path = sys._MEIPASS  # PyInstaller trích xuất tài nguyên tạm thời
    except AttributeError:
        base_path = os.path.abspath(".")  # Khi chạy trực tiếp từ mã nguồn

    return os.path.join(base_path, relative_path)

icon = decrypt_image('logo', (256, 256))
pygame.display.set_icon(icon)
pygame.display.set_caption('Chess_Python by Nguyen Le Van Dung')

if __name__ == '__main__':
    main_menu()
