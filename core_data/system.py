from core_data import *

pygame.init()


def draw_game_state(screen, game_state, square_selected, SQ_SIZE):
    """Vẽ bộ hiện của trò chơi"""
    draw_board(screen, SQ_SIZE)
    highlight_squares(screen, game_state, square_selected, SQ_SIZE)
    if game_state.in_check:
        king_position = game_state.find_king(game_state.white_to_move)
        highlight_king_in_check(screen, king_position, SQ_SIZE)
    draw_pieces(screen, game_state.board, SQ_SIZE)
    draw_captured_pieces(screen, game_state.white_captured_pieces, game_state.black_captured_pieces, SQ_SIZE)
    if square_selected != ():
        row, col = square_selected
        piece = game_state.board[row][col]
        if (piece[0] == 'w' and game_state.white_to_move) or (
        piece[0] == 'b' and not game_state.white_to_move, SQ_SIZE):
            valid_moves = game_state.get_valid_moves()
            highlight_valid_moves(screen, valid_moves, square_selected, SQ_SIZE)
    draw_move_log(screen, game_state, SQ_SIZE)


def load_images(SQ_SIZE):
    """Tải ảnh các quân cờ trên bàn cờ"""
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP',
              'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP']
    for piece in pieces:
        images[piece] = decrypt_image(piece, (SQ_SIZE, SQ_SIZE))


def load_captured_images(SQ_SIZE):
    """Tải ảnh các quân cờ bị ăn"""
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP',
              'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP']
    for piece in pieces:
        captures_images[piece] = decrypt_image(piece, (SQ_SIZE // 2, SQ_SIZE // 2))


def load_promote_images(SQ_SIZE):
    """Tải ảnh quân cần bắt"""
    pieces = ['wQ', 'wR', 'wB', 'wN', 'bQ', 'bR', 'bB', 'bN']
    for piece in pieces:
        promote_images[piece] = decrypt_image(piece, (SQ_SIZE, SQ_SIZE))


def draw_board(screen, SQ_SIZE):
    """Vẽ giao diện bàn cờ"""
    FONT = pygame.font.SysFont('Arial', SQ_SIZE // 4)
    for row in range(8):
        for column in range(8):
            colour = COLOR_A[((row + column) % 2)]
            pygame.draw.rect(screen, colour, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    # Vẽ chữ hàng
    for i in range(8):
        color = COLOR_A[(i % 2)]
        text = FONT.render(chr(ord('a') + i), True, color)
        screen.blit(text, ((SQ_SIZE - SQ_SIZE // 6) + i * SQ_SIZE, SQ_SIZE * 8 - SQ_SIZE // 3))
    # Vẽ chữ cột
    for i in range(8):
        color = COLOR_Z[(i % 2)]
        text = FONT.render(str(8 - i), True, color)
        screen.blit(text, (SQ_SIZE // 25, SQ_SIZE // 25 + i * SQ_SIZE))


def draw_pieces(screen, board, SQ_SIZE):
    """Vẽ quan cờ trên bàn cờ"""
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != '--':
                screen.blit(images[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_captured_pieces(screen, white_captured_pieces, black_captured_pieces, SQ_SIZE):
    """Vẽ các quân cờ đã bị ăn"""
    # Vẽ khung hiển thị quân cờ bị ăn
    draw_button("", 0, SQ_SIZE * 8 + SQ_SIZE // 8, SQ_SIZE,
                SQ_SIZE // 2, SQ_SIZE * 7 - SQ_SIZE // 8, SQ_SIZE // 7, SQ_SIZE // 22,
                'white', 'black', 'wheat3', 'wheat3', 'white')

    draw_button("", 0, SQ_SIZE * 9 - SQ_SIZE // 3,
                SQ_SIZE, SQ_SIZE // 2, SQ_SIZE * 7 - SQ_SIZE // 8, SQ_SIZE // 7, SQ_SIZE // 22,
                'white', 'black', 'wheat3', 'wheat3', 'white')

    # Vẽ quân cờ trắng đã bị ăn
    for i, piece in enumerate(white_captured_pieces):
        piece_image = captures_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (SQ_SIZE * 8 + SQ_SIZE // 8, SQ_SIZE + i * (SQ_SIZE // 2 - SQ_SIZE // 15)))

    # Vẽ quân cờ đen đã bị ăn
    for i, piece in enumerate(black_captured_pieces):
        piece_image = captures_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (SQ_SIZE * 9 - SQ_SIZE // 3, SQ_SIZE + i * (SQ_SIZE // 2 - SQ_SIZE // 15)))


def highlight_king_in_check(screen, king_position, SQ_SIZE):
    """Làm nổi bật vua khi bị chiếu"""
    row, col = king_position
    highlight_king = pygame.Surface((SQ_SIZE, SQ_SIZE))
    highlight_king.set_alpha(100)
    highlight_king.fill(pygame.Color('red'))
    screen.blit(highlight_king, (col * SQ_SIZE, row * SQ_SIZE))


def highlight_squares(screen, game_state, square_selected, SQ_SIZE):
    """Làm nổi bật quân cờ được chọn"""
    # Hiển thị quân cờ đang chọn
    if square_selected != ():
        row, column = square_selected
        if game_state.board[row][column][0] == ('w' if game_state.white_to_move else 'b'):
            highlight_selected = pygame.Surface((SQ_SIZE, SQ_SIZE))
            highlight_selected.set_alpha(100)
            highlight_selected.fill(pygame.Color('black'))
            screen.blit(highlight_selected, (column * SQ_SIZE, row * SQ_SIZE))

    # Hiên thị lịch sử di chuyển quân cờ vừa di chuyển
    if len(game_state.move_log) != 0:
        last_move = game_state.move_log[-1]
        start_row, start_column = last_move.start_row, last_move.start_column
        end_row, end_column = last_move.end_row, last_move.end_column
        highlight_last = pygame.Surface((SQ_SIZE, SQ_SIZE))
        highlight_last.set_alpha(100)
        highlight_last.fill(pygame.Color('orange'))
        screen.blit(highlight_last, (start_column * SQ_SIZE, start_row * SQ_SIZE))
        screen.blit(highlight_last, (end_column * SQ_SIZE, end_row * SQ_SIZE))


def highlight_valid_moves(screen, valid_moves, square_selected, SQ_SIZE):
    """Vẽ các nước đi hợp lệ của quân cờ được chọn, và nước đi ăn quân sẽ là hình tròn rỗng"""
    for move in valid_moves:
        if move.start_row == square_selected[0] and move.start_column == square_selected[1]:
            highlight_moves = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
            highlight_moves.set_alpha(100)
            if move.is_capture:
                pygame.draw.circle(highlight_moves, 'black', (SQ_SIZE // 2, SQ_SIZE // 2),
                                   SQ_SIZE // 3 + SQ_SIZE // 15, SQ_SIZE // 10)
            else:
                pygame.draw.circle(highlight_moves, 'black', (SQ_SIZE // 2, SQ_SIZE // 2), SQ_SIZE // 6)
            screen.blit(highlight_moves, (move.end_column * SQ_SIZE, move.end_row * SQ_SIZE))


def draw_move_log(screen, game_state, SQ_SIZE):
    """Ghi lại nhật ký di chuyển"""
    # Khung hiển thị lich sử di chuyển
    draw_button("", 0, SQ_SIZE * 9 + SQ_SIZE // 4, SQ_SIZE, SQ_SIZE * 5 - SQ_SIZE // 8,
                SQ_SIZE * 7 - SQ_SIZE // 8, SQ_SIZE // 7, 0,
                'white', 'black', COLOR_SCREEN, COLOR_SCREEN, COLOR_SCREEN)

    font_game = pygame.font.Font(font_path, SQ_SIZE // 6)
    move_log_area = pygame.Rect(SQ_SIZE * 9 + SQ_SIZE // 3, SQ_SIZE + SQ_SIZE // 12,
                                SQ_SIZE * 5 - SQ_SIZE // 8, SQ_SIZE * 7 - SQ_SIZE // 8)

    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = f'{i // 2 + 1}. {str(move_log[i])} '
        if i + 1 < len(move_log):
            move_string += f'{str(move_log[i + 1])} '
        move_texts.append(move_string)

    move_padding = 3
    text_y = move_padding
    for j in range(0, len(move_texts), 3):
        text_line = '|'.join(move_texts[j:j + 3])
        text_object = font_game.render(text_line, True, pygame.Color('white'))
        text_location = move_log_area.move(move_padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height()


def animate_move(move, screen, board, clock, game_state, SQ_SIZE):
    """Hoạt ảnh di chuyển quân cờ"""
    delta_row = move.end_row - move.start_row
    delta_column = move.end_column - move.start_column
    total_duration = 0.3
    total_frames = int(clock.get_fps() * total_duration)

    if total_frames == 0:
        total_frames = 1
    for frame in range(total_frames + 1):
        row, column = (
            move.start_row + delta_row * frame / total_frames,
            move.start_column + delta_column * frame / total_frames)
        draw_board(screen, SQ_SIZE)
        draw_pieces(screen, board, SQ_SIZE)
        draw_captured_pieces(screen, game_state.white_captured_pieces, game_state.black_captured_pieces, SQ_SIZE)
        draw_move_log(screen, game_state, SQ_SIZE)

        colour = COLOR_A[(move.end_row + move.end_column) % 2]
        end_square = pygame.Rect(move.end_column * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, colour, end_square)

        if move.piece_captured != '--':
            if move.is_en_passant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = pygame.Rect(move.end_column * SQ_SIZE, en_passant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(images[move.piece_captured], end_square)

        screen.blit(images[move.piece_moved], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
