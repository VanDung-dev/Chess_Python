from interface import *
from data.decryption import decryption_logo

pygame.init()


# Hàm để lấy đường dẫn tài nguyên khi đóng gói bằng PyInstaller
def resource_path(relative_path):
    """Lấy đường dẫn tới file tài nguyên khi chạy từ file"""
    base_path = os.path.abspath(".")  # Khi chạy trực tiếp từ mã nguồn
    return os.path.join(base_path, relative_path)

icon = decryption_logo('logo', (256, 256))
pygame.display.set_icon(icon)
pygame.display.set_caption('Chess_Python by Nguyen Le Van Dung')


if __name__ == '__main__':
    try:
        main_menu()
    except Exception as e:
        pass
