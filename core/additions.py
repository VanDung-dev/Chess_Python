import datetime
from core.constants import *
from data import texts
from data.decryption import decryption_video
from data.save_selection import *


def handle_exit(size, index, other):
    global yes_action
    from interface import main_menu
    """Kiểm tra xem người chơi có muốn thoát game hay quay lại màn hình chính"""
    title_text = ''
    text_size = size // 3
    in_loop = True
    while in_loop:
        # Nội dung và thông điệp tuỳ thuộc vào 'other'
        if other == "quit":  # Quit game
            title_text = texts["Quit game"][index]
            yes_action = lambda: (pygame.quit(), quit())
        elif other == "back":  # Back to main menu
            title_text = texts["Back to main menu"][index]
            yes_action = lambda: (save_preferences_setting(size_index, index, color_index, piece_index),
                                  save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black),
                                  main_menu())

        # Vẽ giao diện
        draw_button("", 0, size * 4, size * 3,
                    size * 6, size * 2, size // 7, size // 15,
                    'white', 'black', color_screen, color_screen, 'aquamarine')
        draw_button(title_text, text_size, size * 7 - size // 4,
                    size * 3 + size // 2, size // 2, size // 2, size // 7, 0,
                    'white', 'white', color_screen, color_screen, color_screen)
        yes_button = draw_button(texts["Yes"][index], text_size,
                                 size * 5 + size // 8, size * 4 + size // 4,
                                 size * 2 - size // 4, size // 2, size // 7, size // 22,
                                 'white', 'black', color_screen, 'tomato', 'tomato')
        no_button = draw_button(texts["No"][index], text_size,
                                size * 7 + size // 8, size * 4 + size // 4,
                                size * 2 - size // 4, size // 2, size // 7, size // 22,
                                'white', 'black', color_screen, 'light green', 'light green')

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                if other == 1:  # Back to main menu gọi quit game nếu người dùng tắt
                    handle_exit(size, index, other="quit")
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if no_button.collidepoint(event.pos):
                    if other == 0:
                        save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                    return
                elif yes_button.collidepoint(event.pos):
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                    yes_action()

        clock_game.tick(60)
        pygame.display.flip()


def draw_button(text, text_size, x, y, w, h, border_radius, border_width,
                not_text_hover_color, text_hover_color, not_hover_color, hover_color, border_color):
    """Vẽ nút bo góc với màu sắc, viền và vị trí đã chỉ định"""
    font_game = pygame.font.Font(font_path, text_size)
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, w, h)

    # Kiểm tra xem chuột có nằm trong nút không
    if button_rect.collidepoint(mouse_pos):
        button_color = hover_color
        text_color = text_hover_color
    else:
        button_color = not_hover_color
        text_color = not_text_hover_color

    # Vẽ viền của nút (nếu có border_width > 0)
    if border_width > 0:
        border_rect = button_rect.inflate(border_width, border_width)
        pygame.draw.rect(screen_game, border_color, border_rect, border_radius=border_radius)

    # Vẽ hình chữ nhật bo góc cho nút
    pygame.draw.rect(screen_game, button_color, button_rect, border_radius=border_radius)

    # Vẽ text của nút ở vị trí trung tâm
    text_surface = font_game.render(text, True, text_color)
    screen_game.blit(text_surface, text_surface.get_rect(center=button_rect.center))

    return button_rect


def code_version(size, index):
    """🤑🤑🤑"""
    in_version = True
    input_text = ""
    cursor_pos = 0
    cursor_visible = True
    cursor_blink_time = 500
    last_blink_time = pygame.time.get_ticks()
    typing_active = False
    typing_timeout = 1000
    backspace_held = False
    backspace_hold_time = 150
    last_backspace_time = pygame.time.get_ticks()
    show_message = False
    message_text = ""
    video = ""
    message_start_time = 0
    message_duration = 3000
    text_size = size // 3

    def check_input_code():
        nonlocal message_text, video, show_message, message_start_time, input_text, cursor_pos
        message_text = texts["Pass"][index] if input_text in ["NGGYU", "TOI"] else texts["Wrong"][
            index]
        video = input_text if input_text in ["NGGYU", "TOI"] else None
        show_message = True
        message_start_time = current_time
        input_text = ""
        cursor_pos = 0

    while in_version:
        current_time = pygame.time.get_ticks()

        # Nếu không nhập ký tự trong thời gian typing_timeout, con trỏ nhấp nháy trở lại
        if not typing_active and current_time - last_blink_time >= cursor_blink_time:
            cursor_visible = not cursor_visible  # Đổi trạng thái con trỏ (hiển thị/ẩn)
            last_blink_time = current_time
        elif typing_active:
            cursor_visible = True  # Khi đang nhập liệu, con trỏ luôn hiển thị

        # Kiểm tra nếu giữ phím BACKSPACE
        if backspace_held and current_time - last_backspace_time >= backspace_hold_time:
            if cursor_pos > 0:
                input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                cursor_pos -= 1
            last_backspace_time = current_time

        # Vẽ nút và các thông báo thoát game
        draw_button("", 0, size * 4, size * 2, size * 6, size * 3, size // 5, size // 10,
                    'white','black', color_screen, color_screen, 'aquamarine')
        text_button = draw_button("", 0, size * 5, size * 2 + size // 2,
                                  size * 4, size, size // 7, size // 10,
                                  'white', 'black', 'white', 'white', 'aquamarine')
        send_button = draw_button(texts["Send"][index], text_size,
                                  size * 5 - size // 4, size * 4 + size // 4,
                                  size * 2, size // 2, size // 7, size // 20,
                                  'white', 'black', color_screen, 'aquamarine', 'aquamarine')
        quit_button = draw_button(texts["Quit"][index], text_size,
                                  size * 7 + size // 4, size * 4 + size // 4,
                                  size * 2, size // 2, size // 7, size // 20,
                                  'white', 'black', color_screen, 'tomato', 'tomato')

        # Hiển thị văn bản nhập vào ở vị trí của text_button
        font = pygame.font.Font(font_path, text_size)
        text_surface = font.render(input_text, True, 'black')
        text_rect = text_surface.get_rect(center=text_button.center)
        screen_game.blit(text_surface, text_rect.topleft)

        # Hiển thị con trỏ (dấu nháy) nếu đang ở trạng thái hiển thị
        if cursor_visible:
            cursor_x = text_rect.x + font.size(input_text[:cursor_pos])[0]
            cursor_y = text_rect.y
            pygame.draw.rect(screen_game, 'black', pygame.Rect(cursor_x, cursor_y, 2, text_rect.height))

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if send_button.collidepoint(event.pos):
                    check_input_code()
                elif quit_button.collidepoint(event.pos):
                    in_version = False

            elif event.type == pygame.KEYDOWN:
                typing_active = True
                last_blink_time = current_time
                if event.key == pygame.K_BACKSPACE:
                    if cursor_pos > 0:
                        input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                        cursor_pos -= 1
                    backspace_held = True
                    last_backspace_time = pygame.time.get_ticks()
                elif event.key == pygame.K_RETURN:
                    check_input_code()
                elif event.key == pygame.K_LEFT:
                    if cursor_pos > 0:
                        cursor_pos -= 1
                elif event.key == pygame.K_RIGHT:
                    if cursor_pos < len(input_text):
                        cursor_pos += 1
                else:
                    if len(input_text) < 19:
                        input_text = input_text[:cursor_pos] + event.unicode + input_text[cursor_pos:]
                        cursor_pos += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    backspace_held = False

        # Kiểm tra xem người dùng đã ngừng nhập trong thời gian timeout hay chưa
        if typing_active and current_time - last_blink_time >= typing_timeout:
            typing_active = False

        # Hiển thị thông báo nếu có và kiểm tra thời gian để ẩn
        if show_message and message_text != "":
            if current_time - message_start_time <= message_duration:
                draw_button(message_text, text_size * 2, size * 4, size * 2,
                            size * 6, size * 3, size // 7, size // 10,
                            'white', 'white', color_screen, color_screen, 'aquamarine')
                if message_text == texts["Pass"][index]:
                    decryption_video(video)
                    quit()
            else:
                show_message = False

        pygame.display.flip()


def hello_user(index, time_type):
    """Gửi lời chào tới người dùng"""
    current_hour = datetime.datetime.now().hour
    username = (
        os.getenv("USERNAME") if os.name == 'nt' else # Windows
        (os.getenv("USER") or os.getenv("LOGNAME")) if os.name == 'posix' else # macOS/Linux
        texts["User"][index]
    )
    current_time = (
        texts["Morning"][index] if 5 <= current_hour < 11 else
        texts["Noon"][index] if 11 <= current_hour < 14 else
        texts["Afternoon"][index] if 14 <= current_hour < 17 else
        texts["Evening"][index]
    )
    date_now = datetime.datetime.now().strftime("%d-%m-%Y" if index == 0 else "%m-%d-%Y")
    if time_type == "24h":
        time_now = datetime.datetime.now().strftime("%H:%M")
    else:
        time_now = datetime.datetime.now().strftime("%I:%M %p")

    return current_time, username, time_now, date_now


def get_promotion_piece(piece_color, end_column, size, index):
    """Hiển thị giao diện để người chơi chọn quân cờ để phong cấp (hậu, xe, tượng, mã)."""
    from engine import GameState
    in_promote = True
    promoted_piece = None
    y = size * (0 if GameState().white_to_move else 4)  # Tọa độ y dựa trên bên được phong cấp
    x = end_column * size  # Tọa độ x dựa trên cột kết thúc
    pieces = ['wQ', 'wR', 'wB', 'wN'] if piece_color == 'w' else ['bQ', 'bR', 'bB', 'bN']

    while in_promote:
        # Vẽ nền cho giao diện phong cấp
        draw_button("", 0, x, y, size, size * 4, size // 7, size // 22, color_screen, color_screen, 'gray',
               'gray', 'aquamarine')
        for i, piece in enumerate(pieces):
            screen_game.blit(promote_images[piece], pygame.Rect(x, y + i * size, size, size))
        pygame.display.flip()

        # Xử lý sự kiện chọn quân cờ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit(size, index, other="quit")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Nhấn chuột trái
                mouse_x, mouse_y = event.pos
                if x <= mouse_x < x + size and y <= mouse_y < y + size * 4:
                    selected_index = (mouse_y - y) // size
                    if 0 <= selected_index < len(pieces):
                        promoted_piece = pieces[selected_index]
                        in_promote = False
                        break
    return promoted_piece

