import platform
import pygame
from data.save_selection import load_preferences_ai, load_preferences_setting

def get_scale():
    """Lấy tỉ lệ hiển thị đa nền tảng"""
    system = platform.system()
    if system == "Windows":
        try:
            import ctypes
            user32 = ctypes.windll.user32
            width_scaled, height_scaled = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            user32.SetProcessDPIAware()
            width_original, height_original = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        except Exception:
            return 1, 1

    elif system == "Linux":

        try:
            import subprocess
            output = subprocess.check_output("xrandr | grep '*' | awk '{print $1}'", shell=True)
            width_scaled, height_scaled = map(int, output.decode().strip().split('x'))
            output = subprocess.check_output("xrandr | grep ' connected primary' | awk '{print $4}'", shell=True)
            width_original, height_original = map(int, output.decode().strip().replace('+0+0', '').split('x'))
        except Exception:
            return 1, 1

    elif system == "Darwin":
        try:
            import AppKit
            frame = AppKit.NSScreen.mainScreen().frame()
            width_scaled, height_scaled = frame[2], frame[3]
            width_original, height_original = AppKit.NSScreen.mainScreen().backingScaleFactor() * width_scaled, AppKit.NSScreen.mainScreen().backingScaleFactor() * height_scaled
        except Exception:
            return 1, 1

    else:
        return 1, 1

    return width_scaled / width_original, height_scaled / height_original

size_index, language_index, color_index, piece_index = load_preferences_setting()
lvl_index, not_negamax_white, not_negamax_black = load_preferences_ai()
version = "v0.8.1"
scale_width, scale_height = get_scale()
images = {}
captures_images = {}
promote_images = {}
temp_move = []
color_board = [
    ['#EBECD0', '#739552'],
    ['#D3D3D3', '#8B4513'],
    ['#DCDCDC', '#2F4F4F'],
    ['#FFFDD0', '#654321'],
    ['#FFFFF0', '#808000'],
    ['#F5F5F5', '#3F4F5F'],
]
color_str = [
    ['#739552', '#EBECD0'],  # Xanh là - Trắng nhạt
    ['#8B4513', '#D3D3D3'],  # Nâu đất - Xam nhạt
    ['#2F4F4F', '#DCDCDC'],  # Xanh lam đất - Xám tro
    ['#654321', '#FFFDD0'],  # Nâu sẫm - Kem nhạt
    ['#808000', '#FFFFF0'],  # Xanh olive - Trắng ngà
    ['#4F4F4F', '#F5F5F5'],  # Đen xám - Trắng xám
]
pieces_images = ['0', '1', '2', '3', '4', '5', '6']
sizes = [(960, 540), (1120, 630), (1280, 720), (1440, 810), (1600, 900)]
lvls = [1, 2, 3]
lvl_colors = ['green', 'yellow', 'tomato']
color_screen = '#505050'
lvl = lvls[lvl_index]
width, height = (int(square_size * scale_width) for square_size in sizes[size_index])
square_size = height // 8
screen_game = pygame.display.set_mode((width, height))
clock_game = pygame.time.Clock()
