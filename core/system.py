from core.additions import *
from data.decryption import decryption_image, other_images

pygame.init()

def draw_game_state(screen, game_state, square_selected, size, suggested_move, index):
    """Vẽ bộ hiện của trò chơi"""
    draw_board(screen, size, index)
    highlight_squares(screen, game_state, square_selected, size)
    if game_state.in_check:
        king_position = game_state.find_king(game_state.white_to_move)
        highlight_king_in_check(screen, king_position, size)
    draw_pieces(screen, game_state.board, size)
    if suggested_move:
        highlight_suggested_move(screen, suggested_move, size)
    draw_captured_pieces(screen, game_state.white_captured_pieces, game_state.black_captured_pieces, size)
    if square_selected != ():
        row, col = square_selected
        piece = game_state.board[row][col]
        if (piece[0] == 'w' and game_state.white_to_move) or (
        piece[0] == 'b' and not game_state.white_to_move, size):
            valid_moves = game_state.get_valid_moves()
            highlight_valid_moves(screen, valid_moves, square_selected, size)


def load_images(size, piece_index):
    """Tải ảnh các quân cờ trên bàn cờ"""
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP',
              'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP']
    for piece in pieces:
        temp_image_path = decryption_image((piece + str(piece_index)), (size, size))
        images[piece] = pygame.image.load(temp_image_path)


def load_captured_images(size, piece_index):
    """Tải ảnh các quân cờ bị ăn"""
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP',
              'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP']
    for piece in pieces:
        temp_image_path = decryption_image((piece + str(piece_index)), (size // 2, size // 2))
        captures_images[piece] = pygame.image.load(temp_image_path)


def load_promote_images(size, piece_index):
    """Tải ảnh quân cần bắt"""
    pieces = ['wQ', 'wR', 'wB', 'wN', 'bQ', 'bR', 'bB', 'bN']
    for piece in pieces:
        temp_image_path = decryption_image((piece + str(piece_index)), (size, size))
        promote_images[piece] = pygame.image.load(temp_image_path)


def load_other_images(size, piece_index):
    """Tải ảnh khác"""
    pieces = ['wK', 'bK']
    for piece in pieces:
        temp_image_path = decryption_image((piece + str(piece_index)), (size // 1.5, size // 1.5))
        other_images[piece] = pygame.image.load(temp_image_path)


def draw_board(screen, size, index):
    """Vẽ giao diện bàn cờ"""
    font_board = pygame.font.Font(font_path, size // 5)
    for row in range(8):
        for column in range(8):
            colour = color_board[index][((row + column) % 2)]
            pygame.draw.rect(screen, colour, pygame.Rect(column * size, row * size, size, size))
    # Vẽ chữ hàng ngang
    for i in range(8):
        color = color_board[index][(i % 2)]
        text = font_board.render(chr(ord('a') + i), True, color)
        screen.blit(text, ((size - size // 6) + i * size, size * 8 - size // 4))
    # Vẽ chữ cột dộc
    for i in range(8):
        color = color_str[index][(i % 2)]
        text = font_board.render(str(8 - i), True, color)
        screen.blit(text, (size // 30, size // 100 + i * size))


def draw_pieces(screen, board, size):
    """Vẽ quan cờ trên bàn cờ"""
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != '--':
                screen.blit(images[piece], pygame.Rect(column * size, row * size, size, size))


def draw_captured_pieces(screen, white_captured_pieces, black_captured_pieces, size):
    """Vẽ các quân cờ đã bị ăn"""
    # Vẽ khung hiển thị quân cờ bị ăn
    draw_button("", 0, size * 8 + size // 8, size,
                size // 2, size * 7 - size // 8, size // 7, size // 22,
                'gray', 'gray', 'gray', 'gray', 'aquamarine')

    draw_button("", 0, size * 9 - size // 3,
                size, size // 2, size * 7 - size // 8, size // 7, size // 22,
                'gray', 'gray', 'gray', 'gray', 'aquamarine')

    # Vẽ quân cờ trắng đã bị ăn
    for i, piece in enumerate(white_captured_pieces):
        piece_image = captures_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (size * 8 + size // 8, size + i * (size // 2 - size // 15)))

    # Vẽ quân cờ đen đã bị ăn
    for i, piece in enumerate(black_captured_pieces):
        piece_image = captures_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (size * 9 - size // 3, size + i * (size // 2 - size // 15)))


def draw_other_pieces(screen, size):
    """Vẽ quân cờ khác"""
    for i in range(2):
        piece = 'wK' if i == 0 else 'bK'
        piece_image = other_images.get(piece)
        if piece_image:
            screen.blit(piece_image,
                        (size * 9 - size // 6 + i * (size // 2 + size // 6), size + size // 20))


def highlight_king_in_check(screen, king_position, size):
    """Làm nổi bật vua khi bị chiếu"""
    row, col = king_position
    highlight_king = pygame.Surface((size, size))
    highlight_king.set_alpha(125)
    highlight_king.fill(pygame.Color('red'))
    screen.blit(highlight_king, (col * size, row * size))


def highlight_squares(screen, game_state, square_selected, size):
    """Làm nổi bật quân cờ được chọn"""
    # Hiển thị quân cờ đang chọn
    if square_selected != ():
        row, column = square_selected
        if game_state.board[row][column][0] == ('w' if game_state.white_to_move else 'b'):
            highlight_selected = pygame.Surface((size, size))
            highlight_selected.set_alpha(125)
            highlight_selected.fill(pygame.Color('black'))
            screen.blit(highlight_selected, (column * size, row * size))

    # Hiên thị lịch sử di chuyển quân cờ vừa di chuyển
    if len(game_state.move_log) != 0:
        last_move = game_state.move_log[-1]
        start_row, start_column = last_move.start_row, last_move.start_column
        end_row, end_column = last_move.end_row, last_move.end_column
        highlight_last = pygame.Surface((size, size))
        highlight_last.set_alpha(125)
        highlight_last.fill(pygame.Color('orange'))
        screen.blit(highlight_last, (start_column * size, start_row * size))
        screen.blit(highlight_last, (end_column * size, end_row * size))


def highlight_valid_moves(screen, valid_moves, square_selected, size):
    """Vẽ các nước đi hợp lệ của quân cờ được chọn, và nước đi ăn quân sẽ là hình tròn rỗng"""
    for move in valid_moves:
        if move.start_row == square_selected[0] and move.start_column == square_selected[1]:
            highlight_moves = pygame.Surface((size, size), pygame.SRCALPHA)
            highlight_moves.set_alpha(125)
            if move.is_capture:
                pygame.draw.circle(highlight_moves, 'black', (size // 2, size // 2),
                                   size // 3, size // 10)
            else:
                pygame.draw.circle(highlight_moves, 'black', (size // 2, size // 2), size // 6)
            screen.blit(highlight_moves, (move.end_column * size, move.end_row * size))


def highlight_suggested_move(screen, suggested_move, size):
    """Làm nổi bật nước đi gợi ý từ AI."""
    if suggested_move:
        suggested_color = pygame.Color('blue')
        start_row, start_col = suggested_move.start_row, suggested_move.start_col
        end_row, end_col = suggested_move.end_row, suggested_move.end_col
        suggested_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(suggested_surface, suggested_color, pygame.Rect(
            start_col * size, start_row * size, size, size), size // 10)
        end_center = (end_col * size + size // 2, end_row * size + size // 2)
        pygame.draw.circle(suggested_surface, suggested_color, end_center, size // 4, size // 10)
        suggested_surface.set_alpha(125)
        screen.blit(suggested_surface, (0, 0))


def animate_move(move, screen, board, clock, game_state, size, index):
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
        draw_board(screen, size, index)
        draw_pieces(screen, board, size)
        draw_captured_pieces(screen, game_state.white_captured_pieces, game_state.black_captured_pieces, size)

        colour = color_board[index][(move.end_row + move.end_column) % 2]
        end_square = pygame.Rect(move.end_column * size, move.end_row * size, size, size)
        pygame.draw.rect(screen, colour, end_square)

        if move.piece_captured != '--':
            if move.is_en_passant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = pygame.Rect(move.end_column * size, en_passant_row * size, size, size)
            screen.blit(images[move.piece_captured], end_square)

        screen.blit(images[move.piece_moved], pygame.Rect(column * size, row * size, size, size))
        pygame.display.flip()

