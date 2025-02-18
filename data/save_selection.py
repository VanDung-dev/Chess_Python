import json
import os
import pygame
from data.decryption import decryption_font
from data.cache_data import get_cache_dir

font_path = decryption_font("FontCustom")
preferences_setting_path = os.path.join(get_cache_dir(), "preferences_setting.json")
preferences_ai_path = os.path.join(get_cache_dir(), "preferences_ai.json")


def save_preferences_setting(size_index, language_index, color_index, piece_index):
    """Cập nhật toàn bộ dữ liệu cài đặt vào preferences_setting.json."""
    os.makedirs(os.path.dirname(preferences_setting_path), exist_ok=True)
    new_data_setting = {
        "size_index": size_index,
        "language_index": language_index,
        "lvl_index": color_index,
        "piece_index": piece_index
    }
    with open(preferences_setting_path, "w") as file_temp:
        json.dump(new_data_setting, file_temp, indent=4)


def save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black):
    """Cập nhật toàn bộ dữ liệu AI vào preferences_ai.json."""
    os.makedirs(os.path.dirname(preferences_ai_path), exist_ok=True)
    new_data_ai = {
        "lvl_index": lvl_index,
        "not_negamax_white": not_negamax_white,
        "not_negamax_black": not_negamax_black
    }
    with open(preferences_ai_path, "w") as file_temp:
        json.dump(new_data_ai, file_temp, indent=4)


def save_move_log(game_state, temp_log):
    """Ghi lại nhật ký di chuyển."""
    move_log = game_state.move_log
    move_texts = []

    # Duyệt qua từng cặp nước đi và chuyển chúng thành chuỗi
    for i in range(0, len(move_log), 2):
        move_string = f"{i // 2 + 1}. {str(move_log[i])} "
        if i + 1 < len(move_log):
            move_string += f"- {str(move_log[i + 1])}"
        move_texts.append(move_string)

    # Chia nhật ký di chuyển thành các trang, mỗi trang tối đa 10 dòng
    max_lines_per_page = 10
    temp_pages = [move_texts[i:i + max_lines_per_page] for i in range(0, len(move_texts), max_lines_per_page)]

    # Xóa dữ liệu cũ trong temp_move và lưu các trang mới
    temp_log.clear()
    temp_log.extend(temp_pages)


def load_preferences_setting():
    """Đọc dữ liệu cài đặt từ preferences_setting.json và trả về các giá trị."""
    try:
        if os.path.exists(preferences_setting_path):
            with open(preferences_setting_path, "r") as file_temp:
                temp_data_part1 = json.load(file_temp)

            size_index = temp_data_part1.get("size_index", 0)
            language_index = temp_data_part1.get("language_index", 0)
            color_index = temp_data_part1.get("lvl_index", 0)
            piece_index = temp_data_part1.get("piece_index", 0)

            return size_index, language_index, color_index, piece_index
        else:
            raise FileNotFoundError

    except FileNotFoundError:
        os.makedirs(os.path.dirname(preferences_setting_path), exist_ok=True)

        default_data_part1 = {
            "size_index": 3,
            "language_index": 0,
            "lvl_index": 0,
            "piece_index": 0
        }

        with open(preferences_setting_path, "w") as file_temp:
            json.dump(default_data_part1, file_temp, indent=4)

        return 3, 0, 0, 0


def load_preferences_ai():
    """Đọc dữ liệu sở thích AI từ preferences_ai.json và trả về các giá trị."""
    try:
        if os.path.exists(preferences_ai_path):
            with open(preferences_ai_path, "r") as file_temp:
                temp_data_part2 = json.load(file_temp)

            lvl_index = temp_data_part2.get("lvl_index", 0)
            not_negamax_white = temp_data_part2.get("not_negamax_white", True)
            not_negamax_black = temp_data_part2.get("not_negamax_black", True)

            return lvl_index, not_negamax_white, not_negamax_black
        else:
            raise FileNotFoundError

    except FileNotFoundError:
        os.makedirs(os.path.dirname(preferences_ai_path), exist_ok=True)
        default_data_part2 = {
            "lvl_index": 1,
            "not_negamax_white": True,
            "not_negamax_black": True
        }
        with open(preferences_ai_path, "w") as file_temp:
            json.dump(default_data_part2, file_temp, indent=4)

        return 1, True, True


def load_move_log(screen, size, page_index, temp_log):
    """Hiển thị các nước đi."""
    font_game = pygame.font.Font(font_path, size // 5 + size // 30)

    # Định nghĩa vùng hiển thị cho nhật ký di chuyển
    move_log_area = pygame.Rect(size * 11 - size // 3, size * 3 + size // 2,
                                size * 5 - size // 2, size * 5)

    # Kiểm tra nếu temp_move có dữ liệu và đảm bảo page_index không vượt quá giới hạn
    if temp_log and page_index >= len(temp_log):
        page_index = len(temp_log) - 1

    # Kiểm tra nếu temp_move có dữ liệu ở trang hiện tại
    if temp_log and 0 <= page_index < len(temp_log):
        display_page = temp_log[page_index]
        move_padding = size // 10
        text_y = move_padding

        # Duyệt qua các nước đi và hiển thị từng dòng
        for move in display_page:
            text_object = font_game.render(move, True, pygame.Color('white'))
            text_location = move_log_area.move(move_padding, text_y)
            screen.blit(text_object, text_location)
            text_y += text_object.get_height()

    # Hiển thị số trang hiện tại
    page_text = f"Trang {page_index + 1 if temp_log else 0}/{len(temp_log)}"
    page_object = font_game.render(page_text, True, pygame.Color('white'))
    screen.blit(page_object, (size * 11 + size // 3, size * 7 + size // 3))
