import time
from engine import *
from negamaxAT import *
from core.system import *
from data.save_selection import *
from data.decryption import decryption_sound

pygame.init()
game_state = GameState()


def new_game(size, size_index, language_index, color_index, piece_index,
             lvl_index, not_negamax_white, not_negamax_black):
    """Kiểm tra xem người chơi có muốn chơi ván mới hay không"""
    text_size = size // 3
    in_new = True
    while in_new:
        # Vẽ nút và các thông báo thoát game
        draw_button("", 0, size * 4, size * 3,
                    size * 6, size * 2, size // 7, size // 10,
                    'white', 'black', color_screen, color_screen, 'aquamarine')
        draw_button(texts["Start new game"][language_index], text_size, size * 7 - size // 4,
                    size * 3 + size // 2, size // 2, size // 2, size // 7, 0,
                    'white', 'white', color_screen, color_screen, color_screen)
        yes_button = draw_button(texts["Yes"][language_index], text_size, size * 5 + size // 8,
                                 size * 4 + size // 4,
                                 size * 2 - size // 4, size // 2, size // 7, size // 20,
                                'white', 'black', color_screen, 'tomato', 'tomato')
        no_button = draw_button(texts["No"][language_index], text_size, size * 7 + size // 8,
                                size * 4 + size // 4,
                                size * 2 - size // 4, size // 2, size // 7, size // 20,
                                'white', 'black', color_screen, 'light green', 'light green')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit(size, language_index, other="quit")
                in_new = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if no_button.collidepoint(event.pos):
                    return
                elif yes_button.collidepoint(event.pos):
                    save_preferences_setting(size_index, language_index, color_index, piece_index)
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                    choose_player(size, size_index, language_index, color_index, piece_index)

        clock_game.tick(60)
        pygame.display.flip()


def support(size, size_index, language_index, color_index, piece_index,
            lvl_index, not_negamax_white, not_negamax_black):
    """Hiển thị cửa sổ hỗ trợ"""
    global width, height, screen_game, apply_settings, lvl
    apply_settings = True
    lvl = lvls[lvl_index]
    notification_time = None
    in_support = True
    text_size = size // 3
    while in_support:
        lvl_color = lvl_colors[lvl_index]

        # Vẽ giao diện hỗ trợ tại đây
        draw_button("", 0, size * 2, size,
                    size * 10, size * 5 + size // 2, size // 7, size // 10,
                    'white', 'white', color_screen, color_screen, 'aquamarine')

        # Viền 1: thông tin
        draw_button("", 0, size * 2 + size // 4, size + size // 4,
                    size * 7 - size // 2, size * 3, size // 7, size // 20,
                    'white', 'white', color_screen, color_screen, 'grey')

        # Tạo font chữ
        font_support = pygame.font.Font(font_path, text_size)
        font_key = pygame.font.Font(font_path, text_size - size // 10)
        font_version = pygame.font.Font(font_path, text_size - size // 8)

        # Tạo các dòng văn bản
        text_support = font_support.render(f'{texts["Support keys"][language_index]}:', True, 'white')
        u_support = font_key.render(f'U: {texts["Undo key"][language_index]}', True, 'white')
        n_support = font_key.render(f'N: {texts["Negamax key"][language_index]}', True, 'white')
        r_support = font_key.render(f'R: {texts["Restart key"][language_index]}', True, 'white')
        text_version = font_version.render(version, True, 'white')

        # Hiển thị các dòng văn bản tại vị trí text_support
        screen_game.blit(text_support, (size * 2 + size // 2, size + size // 2))
        screen_game.blit(u_support, (size * 3, size * 2))
        screen_game.blit(n_support, (size * 3, size * 2 + size // 2))
        screen_game.blit(r_support, (size * 3, size * 3))
        screen_game.blit(text_version, (size * 7, size * 4 - size // 4))

        # Viền 2: nút bấm
        draw_button("", 0, size * 9 + size // 4, size + size // 4,
                    size * 2 + size // 2, size * 3, size // 7, size // 20,
                    'white', 'white', color_screen, color_screen, 'grey')
        resume_button = draw_button(texts["Resume"][language_index], text_size,
                                    size * 10 - size // 2, size + size // 2,
                                    size * 2, size // 2, size // 7, 0,
                                    'white', 'black', color_screen, 'aquamarine', color_screen)
        mew_game_button = draw_button(texts["New game"][language_index], text_size,
                                      size * 10 - size // 2, size * 2 + size // 2,
                                      size * 2, size // 2, size // 7, 0,
                                      'white', 'black', color_screen, 'aquamarine', color_screen)
        main_menu_button = draw_button(texts["Main menu"][language_index], text_size,
                                       size * 10 - size // 2, size * 3 + size // 2,
                                       size * 2, size // 2, size // 7, 0,
                                       'white', 'black', color_screen, 'aquamarine', color_screen)

        # Viện 3: lvl_index AI
        draw_button("", 0, size * 2 + size // 4, size * 4 + size // 2,
                    size * 9 + size // 2, size * 2 - size // 4, size // 7, size // 20,
                    'white', 'white', color_screen, color_screen, 'grey')
        draw_button("", 0, size * 2 + size // 2, size * 5 - size // 4,
                    size * 6 + size // 4, size // 2, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button(texts["Difficulty"][language_index], text_size,
                    size * 2 + size // 2, size * 5 - size // 4,
                    size * 2 + size // 2, size // 2, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_lvl_button = draw_button('<', text_size, size * 5 + size // 2, size * 5 - size // 4,
                                       size // 2, size // 2, size // 7, 0,
                                       'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        draw_button(f'{texts["Level"][language_index]} {lvls[lvl_index]}', text_size,
                    size * 6 + size // 4, size * 5 - size // 4,
                    size + size // 2, size // 2, size // 7, 0,
                    'black', 'black', lvl_color, lvl_color, color_screen)
        plus_lvl_button = draw_button('>', text_size, size * 8, size * 5 - size // 4,
                                      size // 2, size // 2, size // 7, 0,
                                      'black', 'black', 'aquamarine', 'aquamarine', color_screen)

        # Nút khác
        apply_button = draw_button(texts["Apply"][language_index], text_size,
                                   size * 9 + size // 2, size * 5 - size // 4,
                                   size * 2, size // 2, size // 7, size // 20,
                                   'white', 'black', color_screen, 'light green', 'light green')
        support_button = draw_button('≡', text_size, size * 13 + size // 4, size // 4,
                                     size / 2, size // 2, size // 5, 0,
                                     'white', 'black', color_screen, 'white', 'black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit(size, language_index, other="quit")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Phím tùy chọn
                if resume_button.collidepoint(event.pos):
                    if apply_settings == False:
                        notification_time = time.time()
                    else:
                        return lvl_index
                elif mew_game_button.collidepoint(event.pos):
                    if apply_settings == False:
                        notification_time = time.time()
                    else:
                        new_game(size, size_index, language_index, color_index, piece_index, lvl_index,
                                 not_negamax_white, not_negamax_black)
                elif main_menu_button.collidepoint(event.pos):
                    handle_exit(size, language_index, other="back")

                # Điều chỉnh cấp độ AI
                elif minus_lvl_button.collidepoint(event.pos) and event.button == 1 and lvl_index > 0:
                    lvl_index = (lvl_index - 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    apply_settings = False
                elif plus_lvl_button.collidepoint(event.pos) and event.button == 1 and lvl_index < len(lvls) - 1:
                    lvl_index = (lvl_index + 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    apply_settings = False

                # Phím khác
                elif apply_button.collidepoint(event.pos):
                    apply_settings = True
                elif support_button.collidepoint(event.pos):
                    screen_game.fill(color_screen)
                    if apply_settings == False:
                        notification_time = time.time()
                    else:
                        return lvl_index

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if apply_settings == False:
                        notification_time = time.time()
                    else:
                        return lvl_index

        if lvl_index == 2:
            draw_button(texts["Warning"][language_index], text_size, size * 3, size * 5 + size // 2,
                        size * 8, size // 2, 0, 0,
                        'orange red', 'orange red', color_screen, color_screen, 'gray')
        else:
            draw_button("", text_size, size * 3, size * 5 + size // 2,
                        size * 8, size // 2, size // 7, 0,
                        'orange red', 'orange red', color_screen, color_screen, 'gray')

        if notification_time:
            elapsed_time = time.time() - notification_time
            if elapsed_time < 3:
                draw_button(texts["Apply first"][language_index], text_size, size * 3, size * 5 + size // 2,
                            size * 8, size // 2, 0, 0,
                            'orange red', 'orange red', color_screen, color_screen, 'gray')
            else:
                notification_time = None

        clock_game.tick(60)
        pygame.display.flip()


def setting(size, size_index, language_index, color_index, piece_index):
    """Hiển thị menu thiết lập"""
    global width, height, screen_game, apply_settings
    apply_settings = True
    width, height = sizes[size_index]
    notification_time = None
    in_settings = True
    while in_settings:
        text_size = size // 3
        screen_game.fill(color_screen)

        # Chỉnh sửa chủ đề quân cờ
        draw_button("", 0, size * 3, size,
                    size * 8, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button(texts["Theme piece_index"][language_index], text_size, size * 3, size,
                    size * 3, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_piece_button = draw_button('<', text_size, size * 8, size,
                                         size // 2, size // 2 + size // 4, size // 7, 0,
                                         'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        draw_button("", text_size, size * 9 - size // 4, size,
                    size + size // 2, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        plus_piece_button = draw_button('>', text_size, size * 10 + size // 2, size,
                                        size // 2, size // 2 + size // 4, size // 7, 0,
                                        'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        load_other_images(size, piece_index)
        draw_other_pieces(screen_game, size)

        # Chỉnh sửa chủ đề bàn cờ
        draw_button("", 0, size * 3, size * 2,
                    size * 8, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button(texts["Theme board"][language_index], text_size, size * 3, size * 2,
                    size * 3, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_color_button = draw_button('<', text_size, size * 8, size * 2,
                                         size // 2, size // 2 + size // 4, size // 7, 0,
                                        'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        # màu 1
        draw_button("", 0, size * 9 - size // 4, size * 2,
                    size // 2 + size // 4, size // 2 + size // 4, 0, size // 20,
                    'black', 'black', color_board[color_index][0], color_board[color_index][0], 'black')
        # màu 2
        draw_button("", 0, size * 10 - size // 2, size * 2,
                    size // 2 + size // 4, size // 2 + size // 4, 0, size // 20,
                    'black', 'black', color_board[color_index][1], color_board[color_index][1], 'black')
        plus_color_button = draw_button('>', text_size, size * 10 + size // 2, size * 2,
                                        size // 2, size // 2 + size // 4, size // 7, 0,
                                       'black', 'black', 'aquamarine', 'aquamarine', color_screen)

        # Chỉnh sửa kích thước cửa sổ
        draw_button("", 0, size * 3, size * 3,
                    size * 8, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button(texts["Resolution"][language_index], text_size, size * 3, size * 3,
                    size * 3, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_size_button = draw_button('<', text_size, size * 8, size * 3,
                                        size // 2, size // 2 + size // 4, size // 7, 0,
                                        'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        draw_button(f'{width}x{height}', text_size, size * 9 - size // 4, size * 3,
                    size + size // 2, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        plus_size_button = draw_button('>', text_size, size * 10 + size // 2, size * 3,
                                       size // 2, size // 2 + size // 4, size // 7, 0,
                                       'black', 'black', 'aquamarine', 'aquamarine', color_screen)

        # Chỉnh sửa ngôn ngữ
        draw_button("", 0, size * 3, size * 4,
                    size * 8, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button(texts["Language"][language_index], text_size, size * 3, size * 4,
                    size * 3, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_language_button = draw_button('<', text_size, size * 8, size * 4,
                                            size // 2, size // 2 + size // 4, size // 7, 0,
                                            'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        draw_button(f'{texts["English"][language_index]}', text_size, size * 9 - size // 4, size * 4,
                    size + size // 2, size // 2 + size // 4, size // 7, 0,
                    'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        plus_language_button = draw_button('>', text_size, size * 10 + size // 2, size * 4,
                                           size // 2, size // 2 + size // 4, size // 7, 0,
                                           'black', 'black', 'aquamarine', 'aquamarine', color_screen)

        # Các nút còn lại
        back_button = draw_button(texts["Back"][language_index], text_size, size * 8, size * 6,
                                  size * 2, size // 2, size // 7, size // 20,
                                  'white', 'black', color_screen, 'tomato', 'tomato')
        apply_button = draw_button(texts["Apply"][language_index], text_size, size * 4, size * 6,
                                   size * 2, size // 2, size // 7, size // 20,
                                   'white', 'black', color_screen, 'light green', 'light green')
        version_button = draw_button(version, text_size - size // 10, size * 12, size * 7 - size // 4,
                                     size, size // 2, 0, 0,
                                     'white', 'white', color_screen, color_screen, color_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_settings = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Kiểm tra sự kiện thay đổi kích thước cửa sổ
                if minus_size_button.collidepoint(event.pos):
                    if size_index > 0:
                        size_index -= 1
                        width, height = sizes[size_index]
                        apply_settings = False
                elif plus_size_button.collidepoint(event.pos):
                    if size_index < len(sizes) - 1:
                        size_index += 1
                        width, height = sizes[size_index]
                        apply_settings = False

                # Kiểm tra thay đổi màu sắc
                if minus_color_button.collidepoint(event.pos):
                    if color_index > 0:
                        color_index -= 1
                        apply_settings = False
                elif plus_color_button.collidepoint(event.pos):
                    if color_index < len(color_board) - 1:
                        color_index += 1
                        apply_settings = False

                # Kiểm tra sự kiện thay đổi quân cờ
                if minus_piece_button.collidepoint(event.pos):
                    if piece_index > 0:
                        piece_index -= 1
                        apply_settings = False
                elif plus_piece_button.collidepoint(event.pos):
                    if piece_index < len(pieces_images) - 1:
                        piece_index += 1
                        apply_settings = False

                # Kiểm tra thay đổi ngôn ngữ
                if minus_language_button.collidepoint(event.pos):
                    if language_index > 0:
                        language_index -= 1
                elif plus_language_button.collidepoint(event.pos):
                    if language_index < len(texts["Language"]) - 1:
                        language_index += 1

                # Các nút còn lại
                if apply_button.collidepoint(event.pos):
                    WIDTH_NEW, HEIGHT_NEW = sizes[size_index]
                    width = int(WIDTH_NEW * scale_width)
                    height = int(HEIGHT_NEW * scale_width)
                    size = height // 8
                    screen_game = pygame.display.set_mode((width, height))
                    save_preferences_setting(size_index, language_index, color_index, piece_index)
                    apply_settings = True
                elif version_button.collidepoint(event.pos):
                    code_version(size, language_index)
                    screen_game.fill(color_screen)
                elif back_button.collidepoint(event.pos):
                    if apply_settings == False:
                        notification_time = time.time()
                    else:
                        return size_index, language_index, color_index, piece_index

        # Kiểm tra và hiển thị thông báo nếu cần
        if notification_time:
            elapsed_time = time.time() - notification_time
            if elapsed_time < 3:
                draw_button(texts["Apply first"][language_index], text_size, size * 3, size * 7,
                            size * 8, size // 2, size // 7, 0,
                            'orange red', 'orange red', color_screen, color_screen, 'gray')
            else:
                notification_time = None

        clock_game.tick(60)
        pygame.display.update()


def choose_player(size, size_index, language_index, color_index, piece_index):
    """Lựa chọn vị trí chơi cờ"""
    global lvl, text, human_turn, lvl_index, not_negamax_white, not_negamax_black
    text_size = size // 3
    in_choose = True
    while in_choose:
        screen_game.fill(color_screen)
        lvl_colors = ['green', 'yellow', 'orange red']
        lvl_color = lvl_colors[lvl_index]

        player_white_text = texts["Human"][language_index] if not_negamax_white else "Negamax"
        player_white_color = "white" if not_negamax_white else "chartreuse"
        player_black_text = texts["Human"][language_index] if not_negamax_black else "Negamax"
        player_black_color = "white" if not_negamax_black else "chartreuse"

        draw_button(texts["Player white"][language_index], text_size, size * 5, size * 2,
                    size * 2, size // 2, size // 7, 0,
                    'white', 'white', color_screen, color_screen, 'gray')
        white_choose_button = draw_button(player_white_text, text_size, size * 8 - size // 2, size * 2,
                                          size + size // 2, size // 2, size // 7, size // 20,
                                          player_white_color, player_white_color, color_screen, color_screen, 'gray')
        draw_button(texts["Player black"][language_index], text_size, size * 5, size * 3,
                    size * 2, size // 2, size // 7, 0,
                    'white', 'white', color_screen, color_screen, 'gray')
        black_choose_button = draw_button(player_black_text, text_size, size * 8 - size // 2, size * 3,
                                          size + size // 2, size // 2, size // 7, size // 20,
                                          player_black_color, player_black_color, color_screen, color_screen, 'gray')

        draw_button("", 0, size * 3, size * 4, size * 8, size // 2, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        draw_button(texts["Difficulty"][language_index], text_size, size * 3, size * 4,
                    size * 2 + size // 2, size // 2, size // 7, 0,
                    'black', 'black', 'gray', 'gray', 'gray')
        minus_lvl_button = draw_button('<', text_size, size * 8, size * 4,
                                       size // 2, size // 2, size // 7, 0,
                                       'black', 'black', 'aquamarine', 'aquamarine', color_screen)
        draw_button(f'{texts["Level"][language_index]} {lvls[lvl_index]}', text_size,
                    size * 9 - size // 4, size * 4,
                    size + size // 2, size // 2, size // 7, 0,
                    'black', 'black', lvl_color, lvl_color, color_screen)
        plus_lvl_button = draw_button('>', text_size, size * 10 + size // 2, size * 4,
                                      size // 2, size // 2, size // 7, 0,
                                      'black', 'black', 'aquamarine', 'aquamarine', color_screen)

        # Phím khác
        back_button = draw_button(texts["Back"][language_index], text_size, size * 8, size * 6,
                                  size * 2, size // 2, size // 7, size // 20,
                                  'white', 'black', color_screen, 'tomato', 'tomato')
        start_button = draw_button(texts["Start"][language_index], text_size, size * 4, size * 6,
                                   size * 2, size // 2, size // 7, size // 20,
                                   'white', 'black', color_screen, 'light green', 'light green')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Điều chỉnh AI
                if white_choose_button.collidepoint(event.pos):
                    not_negamax_white = not not_negamax_white
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                elif black_choose_button.collidepoint(event.pos):
                    not_negamax_black = not not_negamax_black
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)

                # Điều chỉnh cấp độ AI
                elif minus_lvl_button.collidepoint(event.pos) and lvl_index > 0:
                    lvl_index = (lvl_index - 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                elif plus_lvl_button.collidepoint(event.pos) and lvl_index < len(lvls) - 1:
                    lvl_index = (lvl_index + 1) % len(lvls)
                    lvl = lvls[lvl_index]
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                elif start_button.collidepoint(event.pos):
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                    decryption_sound("game-start")
                    play_game(size, size_index, language_index, color_index, piece_index, lvl_index, not_negamax_white,
                              not_negamax_black)
                elif back_button.collidepoint(event.pos):
                    save_preferences_ai(lvl_index, not_negamax_white, not_negamax_black)
                    return lvl_index, not_negamax_white, not_negamax_black

        if lvl_index == 2:
            draw_button(texts["Warning"][language_index], text_size, size * 3, size * 5, size * 8, size // 2, 0, 0,
                        'orange red', 'orange red', color_screen, color_screen, 'gray')
        else:
            draw_button("", text_size, size * 3, size * 5, size * 8, size // 2, 0, 0,
                        'orange red', 'orange red', color_screen, color_screen, 'gray')

        pygame.display.flip()


def play_game(size, size_index, language_index, color_index, piece_index, lvl_index,
          not_negamax_white, not_negamax_black):
    """Phần giao diện chơi cờ"""
    global width, height, screen_game, lvl, valid_moves, negamax_help, human_move, page_index
    game_state.__init__()
    valid_moves = GameState().get_valid_moves()
    text_size = size // 3
    page_index = 0
    screen_game.fill(color_screen)

    load_images(size, piece_index)
    load_captured_images(size, piece_index)
    load_promote_images(size, piece_index)

    square_selected = ()
    player_clicks = []

    move_made = False
    animate = False
    game_over = False
    sound_played = False
    not_negamax_help = True
    suggested_move = None
    show_suggestion = False
    in_game = True

    while in_game:
        draw_game_state(screen_game, game_state, square_selected, size, suggested_move, color_index)

        human_turn = ((game_state.white_to_move and not_negamax_white) or
                      (not game_state.white_to_move and not_negamax_black))

        # Xác định xử lí tình huống hỗ trợ
        if not_negamax_white and not_negamax_black:
            negamax_help = (not_negamax_white != not_negamax_black) and game_state.white_to_move
        elif not_negamax_white or not_negamax_black:
            negamax_help = (not_negamax_white == not_negamax_black) and game_state.white_to_move

        human_move = human_turn  # Mặc định

        if game_state.stalemate or game_state.stalemate_special():
            text = texts["Stalemate"][language_index]
        elif game_state.checkmate:
            text = (texts["Black win"][language_index] if game_state.white_to_move else
                    texts["White win"][language_index])
        else:
            text = (texts["White Turn"][language_index] if game_state.white_to_move else
                         texts["Black Turn"][language_index])


        draw_button(text, text_size * 2, size * 10 - size // 2, size,
                    size * 4 + size // 2, size * 2, size // 7, size // 20,
                    'white', 'white', color_screen, color_screen,'aquamarine')

        negamax_button = draw_button(texts["AI Help"][language_index], text_size,
                                     size * 8 + size // 2, size // 4,
                                     size * 2, size // 2, size // 7, 0,
                                     'chartreuse', color_screen, color_screen, 'chartreuse', color_screen)
        undo_button = draw_button(texts["Undo"][language_index], text_size, size * 11, size // 4,
                                  size * 2, size // 2, size // 7, 0,
                                  'gold', 'black', color_screen, 'gold', color_screen)
        support_button = draw_button('≡', text_size, size * 13 + size // 4, size // 4,
                                     size / 2, size // 2, size // 5, 0,
                                     'grey', 'black', color_screen, 'grey', color_screen)

        # Khung chứa thông tin nhật ký di chuyển
        draw_button("", 0, size * 10 - size // 2, size * 3 + size // 6, size * 4 + size // 2,
                    size * 5 - size // 4, size // 7, size // 20,
                    'white', 'black', color_screen, color_screen, 'aquamarine')
        minus_page_button = draw_button('<', text_size, size * 10 - size // 3, size * 7 + size // 3,
                                        size + size // 3, size // 2, size // 7, 0, color_screen, color_screen,
                                        'aquamarine', 'aquamarine', color_screen)
        plus_page_button = draw_button('>', text_size, size * 12 + size // 2, size * 7 + size // 3,
                                       size + size // 3, size // 2, size // 7, 0, color_screen, color_screen,
                                       'aquamarine', 'aquamarine', color_screen)

        save_move_log(game_state, temp_move)
        load_move_log(screen_game, square_size, page_index, temp_move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_exit(size, language_index, other="quit")
                screen_game.fill(color_screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if support_button.collidepoint(event.pos):
                    lvl_index = support(size, size_index, language_index, color_index, piece_index, lvl_index,
                                        not_negamax_white, not_negamax_black)
                    lvl = [1, 2, 3][lvl_index]
                    screen_game.fill(color_screen)

                if undo_button.collidepoint(event.pos) and not game_over:
                    if len(game_state.move_log) > 0:
                        for _ in range(2):
                            game_state.undo_move()
                        valid_moves = game_state.get_valid_moves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        show_suggestion = False
                        decryption_sound("move-self")

                if negamax_button.collidepoint(event.pos) and (not_negamax_white or not_negamax_black) and not game_over:
                    not_negamax_help = not not_negamax_help
                    show_suggestion = True
                    human_move = negamax_help
                    decryption_sound("negamax-on")

                if minus_page_button.collidepoint(event.pos):
                    page_index -= 1
                    if page_index < 0:
                        page_index = 0
                if plus_page_button.collidepoint(event.pos):
                    page_index += 1
                    if page_index > 2:
                        page_index = 2

                if not game_over:
                    # Xử lý chọn ô cờ để di chuyển quân cờ
                    location = pygame.mouse.get_pos()
                    column = location[0] // size
                    row = location[1] // size
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
                                game_state.make_move(valid_moves[i], size, language_index)
                                if game_state.castle_move:
                                    decryption_sound("move-self")
                                move_made = True
                                animate = True
                                square_selected = ()
                                player_clicks = []
                                suggested_move = None
                                show_suggestion = False
                        if not move_made:
                            player_clicks = [square_selected]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False
                    lvl_index = support(size, size_index, language_index, color_index, piece_index, lvl_index,
                                        not_negamax_white, not_negamax_black)
                    lvl = [1, 2, 3][lvl_index]
                    screen_game.fill(color_screen)
                elif event.key == pygame.K_n and (not_negamax_white or not_negamax_black):
                    not_negamax_help = not not_negamax_help
                    show_suggestion = True
                    human_move = negamax_help
                    decryption_sound("negamax-on")
                elif event.key == pygame.K_u:
                    if len(game_state.move_log) > 0:
                        for _ in range(2):
                            game_state.undo_move()
                        valid_moves = game_state.get_valid_moves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        show_suggestion = False
                        decryption_sound("move-self")
                elif event.key == pygame.K_r:
                    new_game(size, size_index, language_index, color_index, piece_index, lvl_index,
                             not_negamax_white, not_negamax_black)
                    screen_game.fill(color_screen)

        # Tìm nước đi của AI
        if not game_over and not human_move:
            draw_button(texts["Thinking"][language_index], size // 3, size * 8 + size // 2, size // 4,
                        size * 2, size // 2, size // 7, 0,
                        'white', 'white', color_screen, color_screen, color_screen)
            pygame.display.flip()
            game_state.negamax_turn = True
            set_depth = 4 if lvl_index >= 2 and len(game_state.move_log) > 12 else (
                lvl_index + 3 if lvl_index < 2 else 4)
            if show_suggestion:
                suggested_move = (find_best_move(game_state, valid_moves, size, set_depth, language_index) or
                                  find_random_move(valid_moves))
                game_state.negamax_turn = False
            else:
                AI_move = (find_best_move(game_state, valid_moves, size, set_depth, language_index) or
                           find_random_move(valid_moves))
                game_state.make_move(AI_move, size, language_index)
                if game_state.castle_move:
                    decryption_sound("move-self")
                move_made, animate, game_state.negamax_turn, not_negamax_help = True, True, False, True

        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen_game, game_state.board, clock_game, game_state, size,
                             color_index)
                animate = False
                decryption_sound("move-self")
            valid_moves = game_state.get_valid_moves()
            move_made = False
            page_index = (len(game_state.move_log) + 19) // 20 - 1

        # Kết thúc game
        if (game_state.checkmate or
                game_state.stalemate or
                game_state.stalemate_special()):
            game_over = True

            if not sound_played:
                decryption_sound("game-end")
                sound_played = True

        clock_game.tick(60)
        pygame.display.flip()


def main_menu():
    """Hiển thị menu chính"""
    global width, height,  square_size, screen_game, colors, \
        size_index, language_index, color_index, piece_index, lvl_index, not_negamax_white, not_negamax_black
    running = True
    while running:
        text_size = square_size // 3
        screen_game.fill(color_screen)
        current_time, user_name, time_now, date_now = hello_user(language_index, time_type="24h")
        draw_button(f'{time_now}', text_size * 4, 0, square_size * 2, width, 0, 0, 0,
                    'white', 'white', 'black', 'black', 'grey')
        draw_button(f'{date_now}', text_size, 0, square_size * 3 - square_size // 4, width, 0, 0, 0,
                    'white', 'white', 'black', 'black', 'grey')
        draw_button(f'{current_time}, {user_name}', text_size, 0, square_size * 3 + square_size // 2, width, 0, 0, 0,
                    'white', 'white', 'black', 'black', 'grey')
        draw_button('', 0, square_size * 6 - square_size // 8, square_size * 4 + square_size // 4,
                    square_size * 3 - square_size // 2, square_size * 3, square_size // 7, square_size // 22,
                    'white', 'white', color_screen, color_screen, 'grey')
        play_button = draw_button(texts["New game"][language_index], text_size,
                                  square_size * 6 + square_size // 8, square_size * 4 + square_size // 2,
                                  square_size * 2, square_size // 2, square_size // 7, 0,
                                  'white', 'black', color_screen, 'aquamarine', color_screen)
        setting_button = draw_button(texts["Setting"][language_index], text_size,
                                     square_size * 6 + square_size // 8, square_size * 5 + square_size // 2,
                                     square_size * 2, square_size // 2, square_size // 7, 0,
                                     'white', 'black', color_screen, 'aquamarine', color_screen)
        quit_button = draw_button(texts["Quit"][language_index], text_size,
                                  square_size * 6 + square_size // 8, square_size * 6 + square_size // 2,
                                  square_size * 2, square_size // 2, square_size // 7, 0,
                                  'white', 'black', color_screen, 'tomato', color_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    lvl_index, not_negamax_white, not_negamax_black = (
                        choose_player(square_size, size_index, language_index, color_index, piece_index))
                elif setting_button.collidepoint(event.pos):
                    size_index, language_index, color_index, piece_index = (
                        setting(square_size, size_index, language_index, color_index, piece_index))
                    width, height = (int(size * scale_width) for size in sizes[size_index])
                    square_size = height // 8
                    screen_game = pygame.display.set_mode((width, height))
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        pygame.display.flip()
    pygame.quit()
