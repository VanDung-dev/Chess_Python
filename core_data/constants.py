from base64_encryption import *
import pygame

WIDTH = 1440
HEIGHT = 810

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font_path = decrypt_font("FontCustom")

images = {}
captures_images = {}
promote_images = {}

COLOR_A = ['#ebecd0', '#739552']
COLOR_Z = ['#739552', '#ebecd0']
COLOR_SCREEN = 'grey22'
COLOR_GAME = 'wheat4'

version = "v0.8"
size_index = 3
lvl_index = 1
language_index = 0

texts = {
    # Áp dụng chung
    "Quit": ["Thoát",
             "Quit"],
    "Apply": ["Áp dụng",
              "Apply"],
    "Back": ["Quay lại",
             "Back"],
    "Yes": ["Có",
            "Yes"],
    "No": ["Không",
           "No"],
    "Setting": ["Cài đặt",
                "Setting"],
    "Warning": ["Cảnh báo, trò chơi có thể bị treo!",
                "Warning, the game may freeze!"],
    "New game": ["Trò chơi mới",
                 "New game"],
    "Difficulty": ["Độ khó",
                   "Difficulty"],
    "Level": ["Cấp độ",
              "Level"],

    # Hàm back_to_main_menu
    "Back to main menu": ["Quay lại màn hình chính?",
                          "Back to main menu?"],

    # Hàm code_version
    "Send": ["Gửi",
                  "Send"],
    "Wrong": ["Sai một một",
                   "Wrong code"],
    "Pass": ["Thành công",
             "Pass"],

    # Hàm stale_check

    # Hàm new_game
    "Start new game": ["Chơi ván mới?",
                       "Start new game?"],

    # Hàm support
    "Support keys": ["Các phím hỗ trợ",
                     "Support keys"],
    "Undo key": ["U: Hoàn tác bước đi",
                 "U: Undo the last move"],
    "Negamax key": ["N: Bật/tắt Negamax",
                    "N: Toggle Negamax On/Off"],
    "Restart key": ["R: Chơi lại ván mới",
                    "R: Restart the new game"],
    "Version": ["Phiên bản",
                "Version"],
    "Resume": ["Tiếp tục",
               "Resume"],
    "Main menu": ["Menu chính",
                  "Main menu"],
    "Apply first": ["Vui lòng nhấn \"Áp dụng\" trước",
                    "Please press \"Apply\" first"],

    # Hàm setting
    "Resolution": ["Câu hình",
                   "Resolution"],
    "Language": ["Ngôn ngữ",
                 "Language"],
    "English": ["Tiếng Việt",
                  "English"],
    "Press apply": ["Vui lòng nhấn \"Áp dụng\" trước!",
                    "Please press \"Apply\" first!"],

    # Hàm Choose_player
    "Player white": ["Người chơi trắng",
                     "Player white"],
    "Player black": ["Người chơi đen",
                     "Player black"],
    "Start": ["Chơi",
              "Start"],
    "Human": ["Người",
              "Human"],

    # Hàm play_game
    "AI Help": ["AI hỗ trợ",
                "AI Help"],
    "Undo": ["Hoàn tác",
             "Undo"],
    "Stalemate": ["Hòa cờ",
                  "Stalemate"],
    "Black win": ["Đen Thắng bởi chiếu hết",
                  "Black wins by checkmate"],
    "White win": ["Trắng Thắng bởi chiếu hết",
                  "White wins by checkmate"],
    "Thinking": ["Tìm kiếm...",
                 "Thinking..."],

    # Hàm main_menu
    "Load game": ["Tải trò chơi",
                  "Load game"],

    # Hàm quit_game
    "Quit game": ["Thoát trò chơi?",
                  "Quit game?"],
}
