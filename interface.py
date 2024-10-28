from engine import *
from system import *
from negamaxAI import *
from decryption import *
import time

pygame.init()
version = "v0.7"
size_index = 3
lvl_index = 1
game_state = GameState()

def back_to_main_menu(SQ_SIZE):
    """Kiểm tra xem người chơi có muốn thoát về màn hình chính hay không"""
    in_quit = True
    while in_quit:
        # Vẽ nút và các thông báo thoát game
        draw_button("", 0,SQ_SIZE * 4, SQ_SIZE * 3,
                    SQ_SIZE * 6, SQ_SIZE * 2, SQ_SIZE // 7, SQ_SIZE // 15,
                    'white', 'black', COLOR_SCREEN, COLOR_SCREEN, 'aquamarine')

        draw_button('Are you sure you want to back to main menu?', SQ_SIZE // 4 + SQ_SIZE // 14,
                    SQ_SIZE * 7 - SQ_SIZE // 4,
                    SQ_SIZE * 3 + SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'white', 'white', COLOR_SCREEN, COLOR_SCREEN, COLOR_SCREEN)

        yes_button = draw_button("Yes", SQ_SIZE // 3, SQ_SIZE * 5 + SQ_SIZE // 8, SQ_SIZE * 4 + SQ_SIZE // 4,
                                 SQ_SIZE * 2 - SQ_SIZE // 4, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                 'white', 'black', COLOR_SCREEN, 'tomato', 'tomato')

        no_button = draw_button("No", SQ_SIZE // 3, SQ_SIZE * 7 + SQ_SIZE // 8, SQ_SIZE * 4 + SQ_SIZE // 4,
                                SQ_SIZE * 2 - SQ_SIZE // 4, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                'white', 'black', COLOR_SCREEN, 'light green', 'light green')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if no_button.collidepoint(event.pos):
                    return
                elif yes_button.collidepoint(event.pos):
                    main_menu()

        clock.tick(60)
        pygame.display.flip()

def code_version(SQ_SIZE):
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

    while in_version:
        current_time = pygame.time.get_ticks()

        # Nếu không nhập ký tự trong thời gian typing_timeout, con trỏ nhấp nháy trở lại
        if not typing_active:
            if current_time - last_blink_time >= cursor_blink_time:
                cursor_visible = not cursor_visible
                last_blink_time = current_time
        else:
            cursor_visible = True

        # Kiểm tra nếu giữ phím BACKSPACE
        if backspace_held and current_time - last_backspace_time >= backspace_hold_time:
            if cursor_pos > 0:
                input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                cursor_pos -= 1
            last_backspace_time = current_time

        # Vẽ nút và các thông báo thoát game
        draw_button("", 0, SQ_SIZE * 4, SQ_SIZE * 2,
                    SQ_SIZE * 6, SQ_SIZE * 3, SQ_SIZE // 5, SQ_SIZE // 10,
                    'white', 'black', COLOR_SCREEN, COLOR_SCREEN, 'aquamarine')

        text_button = draw_button("", 0, SQ_SIZE * 5, SQ_SIZE * 2 + SQ_SIZE // 2,
                                  SQ_SIZE * 4, SQ_SIZE, SQ_SIZE // 5, SQ_SIZE // 10,
                                  'white', 'black', 'white', 'white', 'aquamarine')

        send_button = draw_button("Send", SQ_SIZE // 3, SQ_SIZE * 5 - SQ_SIZE // 4, SQ_SIZE * 4 + SQ_SIZE // 4,
                                  SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 5, SQ_SIZE // 15,
                                  'white', 'black', COLOR_SCREEN, 'aquamarine', 'aquamarine')

        quit_button = draw_button("Quit", SQ_SIZE // 3, SQ_SIZE * 7 + SQ_SIZE // 4, SQ_SIZE * 4 + SQ_SIZE // 4,
                                  SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 5, SQ_SIZE // 15,
                                  'white', 'black', COLOR_SCREEN, 'tomato', 'tomato')

        # Hiển thị văn bản nhập vào ở vị trí của text_button
        font = pygame.font.SysFont('Arial', SQ_SIZE // 3 + SQ_SIZE // 15, True)
        text_surface = font.render(input_text, True, 'black')
        text_rect = text_surface.get_rect(center=text_button.center)
        screen.blit(text_surface, text_rect.topleft)

        # Hiển thị con trỏ (dấu nháy) nếu đang ở trạng thái hiển thị
        if cursor_visible:
            cursor_x = text_rect.x + font.size(input_text[:cursor_pos])[0]
            cursor_y = text_rect.y
            pygame.draw.rect(screen, 'black', pygame.Rect(cursor_x, cursor_y, 2, text_rect.height))

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if send_button.collidepoint(event.pos):
                    if input_text == "NGGYU" or input_text == "TOI":
                        message_text = "Pass"
                        video = input_text
                    else:
                        message_text = "Wrong code!"
                    show_message = True
                    message_start_time = current_time
                    input_text = ""
                    cursor_pos = 0

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
                    if input_text == "NGGYU" or input_text == "TOI":
                        message_text = "Pass"
                        video = input_text
                    else:
                        message_text = "Wrong code!"

                    show_message = True
                    message_start_time = current_time
                    input_text = ""
                    cursor_pos = 0
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
                draw_button(message_text, SQ_SIZE // 2, SQ_SIZE * 4, SQ_SIZE * 2,
                            SQ_SIZE * 6, SQ_SIZE * 3, SQ_SIZE // 5, SQ_SIZE // 10,
                            'white', 'white', COLOR_SCREEN, COLOR_SCREEN, 'aquamarine')

                if message_text == "Pass":
                    decrypt_video(video)
                    quit()
            else:
                show_message = False

        pygame.display.flip()

def stale_check(text, SQ_SIZE):
    """Hiển thị thông báo game đã kết thúc"""
    draw_button("", 0, SQ_SIZE * 2, SQ_SIZE * 3,
                SQ_SIZE * 4, SQ_SIZE * 2, SQ_SIZE // 7, SQ_SIZE // 22,
                'white', 'black', COLOR_SCREEN, COLOR_SCREEN, 'aquamarine')

    draw_button(text, SQ_SIZE // 3, SQ_SIZE * 2, SQ_SIZE * 3 + SQ_SIZE // 2,
                SQ_SIZE * 4, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                'white', 'white', COLOR_SCREEN, COLOR_SCREEN, COLOR_SCREEN)

    new_game_button = draw_button("New game", SQ_SIZE // 3, SQ_SIZE * 2 + SQ_SIZE // 8, SQ_SIZE * 4 + SQ_SIZE // 4,
                                  SQ_SIZE * 2 - SQ_SIZE // 4, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                  'white', 'black', COLOR_SCREEN, 'light green', 'light green')

    quit_button = draw_button("Quit", SQ_SIZE // 3, SQ_SIZE * 4 + SQ_SIZE // 8, SQ_SIZE * 4 + SQ_SIZE // 4,
                              SQ_SIZE * 2 - SQ_SIZE // 4, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                              'white', 'black', COLOR_SCREEN, 'tomato', 'tomato')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if new_game_button.collidepoint(event.pos):
                decrypt_sound("game-start")
                play_game(SQ_SIZE, size_index, lvl_index)
            elif quit_button.collidepoint(event.pos):
                main_menu()

def new_game(SQ_SIZE, size_index, lvl_index):
    """Kiểm tra xem người chơi có muốn chơi ván mới hay không"""
    in_new = True
    while in_new:
        # Vẽ nút và các thông báo thoát game
        draw_button("", 0, SQ_SIZE * 4, SQ_SIZE * 3,
                    SQ_SIZE * 6, SQ_SIZE * 2, SQ_SIZE // 7, SQ_SIZE // 15,
                    'white', 'black', COLOR_SCREEN, COLOR_SCREEN, 'aquamarine')

        draw_button('Are you sure you want to play new game?', SQ_SIZE // 4 + SQ_SIZE // 14,
                    SQ_SIZE * 7 - SQ_SIZE // 4,
                    SQ_SIZE * 3 + SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'white', 'white', COLOR_SCREEN, COLOR_SCREEN, COLOR_SCREEN)

        yes_button = draw_button("Yes", SQ_SIZE // 3, SQ_SIZE * 5 + SQ_SIZE // 8, SQ_SIZE * 4 + SQ_SIZE // 4,
                                 SQ_SIZE * 2 - SQ_SIZE // 4, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                 'white', 'black', COLOR_SCREEN, 'tomato', 'tomato')

        no_button = draw_button("No", SQ_SIZE // 3, SQ_SIZE * 7 + SQ_SIZE // 8, SQ_SIZE * 4 + SQ_SIZE // 4,
                                SQ_SIZE * 2 - SQ_SIZE // 4, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                'white', 'black', COLOR_SCREEN, 'light green', 'light green')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if no_button.collidepoint(event.pos):
                    return
                elif yes_button.collidepoint(event.pos):
                    decrypt_sound("game-start")
                    play_game(SQ_SIZE, size_index, lvl_index)
                    return lvl_index

        clock.tick(60)
        pygame.display.flip()

def support(SQ_SIZE, size_index, lvl_index):
    """Hiển thị cửa sổ hỗ trợ"""
    global WIDTH, HEIGHT, screen, apply, lvl
    apply = True
    lvls = [1, 2, 3]
    lvl = lvls[lvl_index]
    sizes = [(960, 540), (1120, 630), (1280, 720), (1440, 810), (1600, 900)]
    WIDTH, HEIGHT = sizes[size_index]
    notification_time = None
    in_support = True
    while in_support:
        lvl_colors = ['green', 'yellow', 'orange red']
        lvl_color = lvl_colors[lvl_index]

        # Vẽ giao diện hỗ trợ tại đây
        draw_button("", 0, SQ_SIZE * 2, SQ_SIZE,
                    SQ_SIZE * 10, SQ_SIZE * 5 + SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 15,
                    'white', 'white', COLOR_SCREEN, COLOR_SCREEN, 'aquamarine')


        # Viền 1: thông tin
        draw_button("", 0, SQ_SIZE * 2 + SQ_SIZE // 4, SQ_SIZE + SQ_SIZE // 4,
                    SQ_SIZE * 7 - SQ_SIZE // 2, SQ_SIZE * 3, SQ_SIZE // 7, SQ_SIZE // 22,
                    'white', 'white', COLOR_SCREEN, COLOR_SCREEN, 'grey')

        # Tạo font chữ
        font_support  = pygame.font.SysFont('Arial', SQ_SIZE // 4)  # Điều chỉnh kích thước font nếu cần

        # Tạo các dòng văn bản
        text_support1 = font_support.render("Support keys:", True, 'white')
        text_support2 = font_support.render("       U: Undo the last move", True, 'white')
        text_support3 = font_support.render("       N: Toggle Negamax On/Off", True, 'white')
        text_support4 = font_support.render("       R: Restart the game", True, 'white')
        text_support7 = font_support.render(f"Version: {version}", True, 'white')

        # Hiển thị các dòng văn bản tại vị trí text_support
        screen.blit(text_support1, (SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE + SQ_SIZE // 2))
        screen.blit(text_support2, (SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE * 2))
        screen.blit(text_support3, (SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE * 2 + SQ_SIZE // 2))
        screen.blit(text_support4, (SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE * 3))
        screen.blit(text_support7, (SQ_SIZE * 7, SQ_SIZE * 4 - SQ_SIZE // 4))

        # Viền 2:: nút bấm
        draw_button("", 0, SQ_SIZE * 9 + SQ_SIZE // 4, SQ_SIZE + SQ_SIZE // 4,
                    SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE * 3, SQ_SIZE // 7, SQ_SIZE // 22,
                    'white', 'white', COLOR_SCREEN, COLOR_SCREEN, 'grey')

        resume_button = draw_button('Resume', SQ_SIZE // 3, SQ_SIZE * 10 - SQ_SIZE // 2, SQ_SIZE + SQ_SIZE // 2,
                                    SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7,0,
                                    'white', 'black', COLOR_SCREEN, 'aquamarine', COLOR_SCREEN)

        mew_game_button = draw_button('New Game', SQ_SIZE // 3,  SQ_SIZE * 10 - SQ_SIZE // 2, SQ_SIZE * 2 + SQ_SIZE // 2,
                                      SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                  'white', 'black', COLOR_SCREEN, 'aquamarine', COLOR_SCREEN)

        main_menu_button = draw_button("Main menu", SQ_SIZE // 3,  SQ_SIZE * 10 - SQ_SIZE // 2, SQ_SIZE * 3 + SQ_SIZE // 2,
                                       SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7,0,
                                  'white', 'black', COLOR_SCREEN, 'aquamarine', COLOR_SCREEN)

        support_button = draw_button('≡', SQ_SIZE // 3, SQ_SIZE * 13 + SQ_SIZE // 4, SQ_SIZE // 4,
                                     SQ_SIZE / 2, SQ_SIZE // 2, SQ_SIZE // 5, 0,
                                     'white', 'black', COLOR_SCREEN, 'white', 'black')


        # Viện 3: lvl AI
        draw_button("", 0, SQ_SIZE * 2 + SQ_SIZE // 4, SQ_SIZE * 4 + SQ_SIZE // 2,
                    SQ_SIZE * 9 + SQ_SIZE // 2, SQ_SIZE * 2 - SQ_SIZE // 4, SQ_SIZE // 7, SQ_SIZE // 22,
                    'white', 'white', COLOR_SCREEN, COLOR_SCREEN, 'grey')

        draw_button("", 0, SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE * 5 - SQ_SIZE // 4,
                    SQ_SIZE * 6 + SQ_SIZE // 4, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button('Negamax Level', SQ_SIZE // 3, SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE * 5 - SQ_SIZE // 4,
                    SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_lvl_button = draw_button('<', SQ_SIZE // 3, SQ_SIZE * 5 + SQ_SIZE // 2, SQ_SIZE * 5 - SQ_SIZE // 4,
                                        SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                        'black', 'black', 'aquamarine', 'aquamarine', COLOR_SCREEN)
        draw_button(f'lvl {lvls[lvl_index]}', SQ_SIZE // 3, SQ_SIZE * 6 + SQ_SIZE // 4, SQ_SIZE * 5 - SQ_SIZE // 4,
                    SQ_SIZE + SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', lvl_color, lvl_color, COLOR_SCREEN)
        plus_lvl_button = draw_button('>', SQ_SIZE // 3, SQ_SIZE * 8, SQ_SIZE * 5 - SQ_SIZE // 4,
                                       SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                       'black', 'black', 'aquamarine', 'aquamarine', COLOR_SCREEN)

        apply_button = draw_button('Apply', SQ_SIZE // 3, SQ_SIZE * 9 + SQ_SIZE // 2, SQ_SIZE * 5 - SQ_SIZE // 4,
                                   SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                   'white', 'black', COLOR_SCREEN, 'light green', 'light green')


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(SQ_SIZE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button.collidepoint(event.pos) or support_button.collidepoint(event.pos):
                    if apply == False:
                        # Hiển thị thông báo yêu cầu nhấn "Apply"
                        notification_time = time.time()
                    else:
                        return lvl_index
                elif mew_game_button.collidepoint(event.pos):
                    if apply == False:
                        # Hiển thị thông báo yêu cầu nhấn "Apply"
                        notification_time = time.time()
                    else:
                        new_game(SQ_SIZE, size_index, lvl_index)
                elif main_menu_button.collidepoint(event.pos):
                    back_to_main_menu(SQ_SIZE)

                elif minus_lvl_button.collidepoint(event.pos) and event.button == 1 and lvl_index > 0:
                    lvl_index = (lvl_index - 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    apply = False
                elif plus_lvl_button.collidepoint(event.pos) and event.button == 1 and lvl_index < len(lvls) - 1:
                    lvl_index = (lvl_index + 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    apply = False

                elif apply_button.collidepoint(event.pos) and event.button == 1:
                    apply = True

                elif support_button.collidepoint(event.pos) and event.button == 1:
                    screen.fill(COLOR_GAME)
                    return lvl_index

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if apply == False:
                        notification_time = time.time()
                    else:
                        return lvl_index

        if lvl_index == 2:
            draw_button("Warning, the game may freeze!", SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 5 + SQ_SIZE // 2,
                        SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                        'orange red', 'orange red', COLOR_SCREEN, COLOR_SCREEN, 'gray')
        else:
            draw_button("", SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 5 + SQ_SIZE // 2,
                        SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                        'orange red', 'orange red', COLOR_SCREEN, COLOR_SCREEN, 'gray')

        if notification_time:
            elapsed_time = time.time() - notification_time
            if elapsed_time < 3:
                draw_button("Please press \"Apply\" first", SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 5 + SQ_SIZE // 2,
                            SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                           'orange red', 'orange red', COLOR_SCREEN, COLOR_SCREEN, 'gray')
            else:
                notification_time = None

        clock.tick(60)
        pygame.display.flip()

def setting(SQ_SIZE, size_index, lvl_index):
    """Hiển thị menu thiết lập"""
    global WIDTH, HEIGHT, screen, apply, lvl
    apply = True
    lvls = [1, 2, 3]
    lvl = lvls[lvl_index]
    sizes = [(960, 540), (1120, 630), (1280, 720), (1440, 810), (1600, 900)]
    WIDTH, HEIGHT = sizes[size_index]
    notification_time = None  # Biến lưu thời gian bắt đầu hiển thị thông báo
    in_settings = True
    screen.fill(COLOR_SCREEN)
    while in_settings:
        # Điều chỉnh màu sắc cho cấp độ
        lvl_colors = ['green','yellow','orange red']
        lvl_color = lvl_colors[lvl_index]

        draw_button("", 0, SQ_SIZE * 3, SQ_SIZE * 3,
                    SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button('Resolution', SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 3,
                    SQ_SIZE * 2 - SQ_SIZE // 12, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_size_button = draw_button('<', SQ_SIZE // 3, SQ_SIZE * 8, SQ_SIZE * 3,
                                      SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                   'black', 'black', 'aquamarine', 'aquamarine', COLOR_SCREEN)
        draw_button(f'{WIDTH}x{HEIGHT}', SQ_SIZE // 3, SQ_SIZE * 9 - SQ_SIZE // 4, SQ_SIZE * 3,
                    SQ_SIZE + SQ_SIZE // 2 , SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', 'aquamarine', 'aquamarine', COLOR_SCREEN)
        plus_size_button = draw_button('>', SQ_SIZE // 3, SQ_SIZE * 10 + SQ_SIZE // 2, SQ_SIZE * 3,
                                     SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                  'black', 'black', 'aquamarine', 'aquamarine', COLOR_SCREEN)

        draw_button("", 0, SQ_SIZE * 3, SQ_SIZE * 4,
                    SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button('Negamax Level', SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 4,
                    SQ_SIZE * 2 + SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_lvl_button = draw_button('<', SQ_SIZE // 3, SQ_SIZE * 8, SQ_SIZE * 4,
                                       SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                   'black', 'black', 'aquamarine', 'aquamarine', COLOR_SCREEN)
        draw_button(f'lvl {lvls[lvl_index]}', SQ_SIZE // 3, SQ_SIZE * 9 - SQ_SIZE // 4, SQ_SIZE * 4,
                    SQ_SIZE + SQ_SIZE // 2 , SQ_SIZE // 2, SQ_SIZE // 7, 0,
                    'black', 'black', lvl_color, lvl_color, COLOR_SCREEN)
        plus_lvl_button = draw_button('>', SQ_SIZE // 3, SQ_SIZE * 10 + SQ_SIZE // 2, SQ_SIZE * 4,
                                      SQ_SIZE // 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                  'black', 'black', 'aquamarine', 'aquamarine', COLOR_SCREEN)

        back_button = draw_button('Back', SQ_SIZE // 3, SQ_SIZE * 8, SQ_SIZE * 6,
                                  SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                  'white', 'black', COLOR_SCREEN, 'tomato', 'tomato')
        apply_button = draw_button('Apply', SQ_SIZE // 3, SQ_SIZE * 4, SQ_SIZE * 6,
                                   SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 22,
                                   'white', 'black', COLOR_SCREEN, 'light green', 'light green')
        version_button = draw_button(version, SQ_SIZE // 4, SQ_SIZE * 12, SQ_SIZE * 7,
                                     SQ_SIZE, SQ_SIZE // 2, SQ_SIZE // 7, SQ_SIZE // 15,
                                     'white', 'white', COLOR_SCREEN, COLOR_SCREEN, COLOR_SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if minus_size_button.collidepoint(event.pos) and event.button == 1 and size_index > 0:
                    size_index = (size_index - 1) % len(sizes)
                    WIDTH, HEIGHT = sizes[size_index]
                    apply = False
                elif plus_size_button.collidepoint(event.pos) and event.button == 1 and size_index < len(sizes) - 1:
                    size_index = (size_index + 1) % len(sizes)
                    WIDTH, HEIGHT = sizes[size_index]
                    apply = False

                elif minus_lvl_button.collidepoint(event.pos) and event.button == 1 and lvl_index > 0:
                    lvl_index = (lvl_index - 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    apply = False
                elif plus_lvl_button.collidepoint(event.pos) and event.button == 1 and lvl_index < len(lvls) - 1:
                    lvl_index = (lvl_index + 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    apply = False

                elif apply_button.collidepoint(event.pos) and event.button == 1:
                    SQ_SIZE = HEIGHT // 8
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Thay đổi kích thước cửa sổ
                    screen.fill(COLOR_SCREEN)
                    apply = True
                elif version_button.collidepoint(event.pos) and event.button == 1:
                    code_version(SQ_SIZE)
                    screen.fill(COLOR_SCREEN)
                elif back_button.collidepoint(event.pos) and event.button == 1:
                    if apply == False:
                        # Hiển thị thông báo yêu cầu nhấn "Apply"
                        notification_time = time.time()
                    else:
                        # Nếu đã bấm "Apply", thực hiện quay lại
                        return size_index, lvl_index, SQ_SIZE

        if lvl_index == 2:
            draw_button("Warning, the game may freeze!", SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 5,
                            SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                            'orange red', 'orange red', COLOR_SCREEN, COLOR_SCREEN, 'gray')
        else:
            draw_button("", SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 5,
                        SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                        'orange red', 'orange red', COLOR_SCREEN, COLOR_SCREEN, 'gray')

        # Kiểm tra và hiển thị thông báo nếu cần
        if notification_time:
            elapsed_time = time.time() - notification_time
            if elapsed_time < 3:
                draw_button("Please press \"Apply\" first", SQ_SIZE // 3, SQ_SIZE * 3, SQ_SIZE * 2,
                            SQ_SIZE * 8, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                            'orange red', 'orange red', COLOR_SCREEN, COLOR_SCREEN, 'gray')
            else:
                notification_time = None

        clock.tick(60)
        pygame.display.flip()

def play_game(SQ_SIZE,size_index, lvl_index):
    """Phần giao diện chơi cờ"""
    global WIDTH, HEIGHT, screen, lvl, text, valid_moves

    game_state.__init__() # Khởi động lại trò chơi
    valid_moves = GameState().get_valid_moves()

    screen.fill(COLOR_GAME)
    move_made = False
    animate = False
    load_images(SQ_SIZE)
    load_captured_images(SQ_SIZE)
    load_promote_images(SQ_SIZE)

    in_game = True
    square_selected = ()
    player_clicks = []
    game_over = False
    sound_played = False
    not_negamax = True

    while in_game:
        human_turn = (game_state.white_to_move and True) or (not game_state.white_to_move and not_negamax)
        # Tạo văn bản "Negamax" với màu trắng
        font = pygame.font.SysFont('Arial', SQ_SIZE // 3, True)
        negamax_text = font.render("Negamax:", True, 'white')

        # Tạo văn bản "on" hoặc "off" với màu tương ứng
        if not_negamax:
            status_text = font.render("Off", True, 'tomato')
        else:
            status_text = font.render("On", True, 'chartreuse')

        # Vẽ nút Negamax (nền)
        negamax_button = draw_button('', SQ_SIZE // 3, SQ_SIZE * 8 + SQ_SIZE // 2, SQ_SIZE // 4,
                                     SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                     'white', 'black', COLOR_SCREEN, COLOR_SCREEN, 'black')

        # Hiển thị văn bản "Negamax" và "on/off" trên nút
        screen.blit(negamax_text, (SQ_SIZE * 9 - SQ_SIZE // 2 + SQ_SIZE // 8, SQ_SIZE // 2 - SQ_SIZE // 5))
        screen.blit(status_text, (SQ_SIZE * 10 - SQ_SIZE // 15, SQ_SIZE // 2 - SQ_SIZE // 5))

        undo_button = draw_button('Undo', SQ_SIZE // 3, SQ_SIZE * 11, SQ_SIZE // 4,
                                  SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                  'gold', 'black', COLOR_SCREEN, 'gold', 'black')

        support_button = draw_button('≡', SQ_SIZE // 3, SQ_SIZE * 13 + SQ_SIZE // 4, SQ_SIZE // 4,
                                     SQ_SIZE / 2, SQ_SIZE // 2, SQ_SIZE // 5, 0,
                                     'grey', 'black', COLOR_SCREEN, 'grey', 'black')

        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game(SQ_SIZE)
                    screen.fill(COLOR_GAME)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if support_button.collidepoint(event.pos):
                        lvl_index = support(SQ_SIZE, size_index, lvl_index)
                        lvl = [1, 2, 3][lvl_index]
                        screen.fill(COLOR_GAME)
                    elif undo_button.collidepoint(event.pos):
                        if len(game_state.move_log) > 0:
                            for _ in range(2):
                                game_state.undo_move()
                            valid_moves = game_state.get_valid_moves()
                            square_selected = ()
                            player_clicks = []
                            move_made = False
                            animate = False
                            decrypt_sound("move-self")
                    elif negamax_button.collidepoint(event.pos):
                        not_negamax = not not_negamax
                        if not_negamax:
                            for _ in range(2):
                                decrypt_sound("negamax-off")
                                pygame.time.delay(100)
                        else:
                            decrypt_sound("negamax-on")

                    if not game_over:
                        location = pygame.mouse.get_pos()
                        column = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if square_selected == (row, column) or column >= 8:
                            square_selected = ()
                            player_clicks = []
                        else:
                            square_selected = (row, column)
                            player_clicks.append(square_selected)
                        if len(player_clicks) == 2:
                            move = Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.make_move(valid_moves[i], SQ_SIZE)
                                    if game_state.castle_move:
                                        decrypt_sound("move-self")
                                    move_made = True
                                    animate = True
                                    square_selected = ()
                                    player_clicks = []

                            if not move_made:
                                player_clicks = [square_selected]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        lvl_index = support(SQ_SIZE, size_index, lvl_index)
                        lvl = [1, 2, 3][lvl_index]
                        screen.fill(COLOR_GAME)
                    elif event.key == pygame.K_n:
                        not_negamax = not not_negamax
                        if not_negamax:
                            for _ in range(2):
                                decrypt_sound("negamax-off")
                                pygame.time.delay(100)
                        else:
                            decrypt_sound("negamax-on")
                    elif event.key == pygame.K_u:
                        if len(game_state.move_log) > 0:
                            for _ in range(2):
                                game_state.undo_move()
                            valid_moves = game_state.get_valid_moves()
                            square_selected = ()
                            player_clicks = []
                            move_made = False
                            animate = False
                            decrypt_sound("move-self")
                    elif event.key == pygame.K_r:
                        decrypt_sound("game-start")
                        new_game(SQ_SIZE, size_index, lvl_index)

        # Tìm nước đi của AI
        if not game_over and not human_turn:
            draw_button('AI thinking...', SQ_SIZE // 3, SQ_SIZE * 8 + SQ_SIZE // 2, SQ_SIZE // 4,
                        SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                        'white', 'white', COLOR_SCREEN, COLOR_SCREEN, 'black')
            pygame.display.flip()
            game_state.negamax_turn = True
            if lvl_index < 2:
                set_depth = lvl_index + 3
            else:
                if len(game_state.move_log) <= 12:
                    set_depth = 4
                else:
                    set_depth = 5
            AI_move = find_best_move(game_state, valid_moves, SQ_SIZE, set_depth)
            if AI_move is None:
                AI_move = find_random_move(valid_moves)
            game_state.make_move(AI_move, SQ_SIZE)
            if game_state.castle_move:
                decrypt_sound("move-self")
            move_made = True
            animate = True
            game_state.negamax_turn = False

        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock, game_state, SQ_SIZE)
                animate = False
                decrypt_sound("move-self")
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_game_state(screen, game_state, square_selected, SQ_SIZE)

        if (game_state.checkmate or
            game_state.stalemate or
            game_state.stalemate_special()):
            game_over = True

            if not sound_played:
                decrypt_sound("game-end")
                sound_played = True

            # Hiển thị kết quả trò chơi
            if game_state.stalemate:
                text = 'Stalemate'
            elif game_state.checkmate:
                if game_state.white_to_move:
                    text = 'Black wins by checkmate'
                else:
                    text = 'White wins by checkmate'
            stale_check(text, SQ_SIZE)

        clock.tick(60)
        pygame.display.flip()

def main_menu():
    """Hiển thị menu chính"""
    running = True
    global WIDTH, HEIGHT, SQ_SIZE, screen, size_index, lvl_index, lvl
    SQ_SIZE = HEIGHT // 8
    screen.fill(COLOR_SCREEN)

    while running:
        draw_button('', SQ_SIZE // 3, SQ_SIZE * 6 - SQ_SIZE // 4, SQ_SIZE * 3 + SQ_SIZE // 4,
                    SQ_SIZE * 3 - SQ_SIZE // 2, SQ_SIZE * 3, SQ_SIZE // 7, SQ_SIZE // 22,
                    'white', 'white', COLOR_SCREEN, COLOR_SCREEN, 'grey')

        play_button = draw_button('New Game', SQ_SIZE // 3, SQ_SIZE * 6, SQ_SIZE * 3 + SQ_SIZE // 2,
                                  SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                  'white', 'black', COLOR_SCREEN, 'aquamarine', COLOR_SCREEN)

        setting_button = draw_button('Setting', SQ_SIZE // 3, SQ_SIZE * 6, SQ_SIZE * 4 + SQ_SIZE // 2,
                                     SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                     'white', 'black', COLOR_SCREEN, 'aquamarine', COLOR_SCREEN)

        quit_button = draw_button('Quit', SQ_SIZE // 3, SQ_SIZE * 6, SQ_SIZE * 5 + SQ_SIZE // 2,
                                  SQ_SIZE * 2, SQ_SIZE // 2, SQ_SIZE // 7, 0,
                                  'white', 'black', COLOR_SCREEN, 'tomato', COLOR_SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    decrypt_sound("game-start")
                    play_game(SQ_SIZE, size_index, lvl_index)
                elif setting_button.collidepoint(event.pos):
                    size_index, lvl_index, SQ_SIZE = setting(SQ_SIZE, size_index, lvl_index)
                    WIDTH, HEIGHT = [(960, 540), (1120, 630), (1280, 720), (1440, 810), (1600, 900)][size_index]
                    lvl = [1, 2, 3][lvl_index]
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    screen.fill(COLOR_SCREEN)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        pygame.display.flip()

    pygame.quit()
