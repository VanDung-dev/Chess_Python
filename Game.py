from Engine import *
from Constants import *
import pygame as p

p.init()

def draw_game_state(screen, game_state, square_selected):
    draw_board(screen)  # Vẽ bàn cờ
    highlight_squares(screen, game_state, square_selected)  # Làm nổi bật ô được chọn và các ô có thể đi được

    # Kiểm tra nếu quân vua bị chiếu và thêm viền đỏ
    if game_state.in_check:
        king_position = game_state.find_king(game_state.white_to_move)  # Lấy vị trí của vua
        highlight_king_in_check(screen, king_position) # Vẽ viền đỏ quanh vua

    draw_pieces(screen, game_state.board)  # Vẽ các quân cờ trên bàn cờ
    draw_captured_pieces(screen, game_state.captured_pieces)  # Vẽ các quân cờ đã bị ăn

    # Hiển thị các nước đi hợp lệ
    if square_selected != ():
        row, col = square_selected
        piece = game_state.board[row][col]
        if (piece[0] == 'w' and game_state.white_to_move) or (piece[0] == 'b' and not game_state.white_to_move):
            valid_moves = game_state.get_valid_moves()
            highlight_valid_moves(screen, game_state, valid_moves, square_selected)

    draw_move_log(screen, game_state)  # Vẽ lịch sử các nước đi

def draw_board(screen):
    """Draw squares on the board using a chess.com colouring pattern"""
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            colour = COLOR_A[((row + column) % 2)]
            p.draw.rect(screen, colour, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    # Vẽ chữ hàng
    for i in range(DIMENSION):
        color = COLOR_A[(i % 2)]
        text = medium_font.render(chr(ord('a') + i), True, color)
        screen.blit(text, (SQ_SIZE * 0.86 + i * SQ_SIZE, SQ_SIZE * 7.7))
    # Vẽ chữ cột
    for i in range(DIMENSION):
        color = COLOR_Z[(i % 2)]
        text = medium_font.render(str(8 - i), True, color)
        screen.blit(text, (SQ_SIZE * 0.05, SQ_SIZE // 25 + i * SQ_SIZE))
    p.draw.rect(screen, 'grey22', p.Rect(SQ_SIZE // 8, SQ_SIZE * 8.1, SQ_SIZE * 7.9, SQ_SIZE // 1.75), 2)
    p.draw.rect(screen, 'grey22', p.Rect(SQ_SIZE // 8, SQ_SIZE * 8.7, SQ_SIZE * 7.9, SQ_SIZE // 1.75), 2)
    p.draw.rect(screen, 'grey22', p.Rect(SQ_SIZE * 8.2, SQ_SIZE - BUTTON_HEIGHT, SQ_SIZE * 4.15, SQ_SIZE // 1.5))
    p.draw.rect(screen, 'dark grey', p.Rect(SQ_SIZE * 10, SQ_SIZE * 9, SQ_SIZE * 3, SQ_SIZE))
    text_version = version_font.render(version, True, p.Color('black'))
    screen.blit(text_version, (SQ_SIZE * 11, SQ_SIZE * 9))

def draw_pieces(screen, board):
    """Draws pieces on the board using the current GameState.board"""
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':  # Add pieces if not an empty square
                screen.blit(images[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_captured_pieces(screen, captured_pieces):
    """Vẽ các quân cờ đã bị ăn theo hàng ngang, quân trắng nằm trên, quân đen nằm dưới"""
    white_captures = [p for p in captured_pieces if p[0] == 'w']
    black_captures = [p for p in captured_pieces if p[0] == 'b']

    # Vẽ quân cờ trắng đã bị ăn (hàng trên)
    for i, piece in enumerate(white_captures):
        piece_image = captures_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (SQ_SIZE // 8 + i * SQ_SIZE // 2, SQ_SIZE * 8.1))

    # Vẽ quân cờ đen đã bị ăn (hàng dưới)
    for i, piece in enumerate(black_captures):
        piece_image = captures_images.get(piece)
        if piece_image:
            screen.blit(piece_image, (SQ_SIZE // 8 + i * SQ_SIZE // 2, SQ_SIZE * 8.7))

def highlight_king_in_check(screen, king_position):
    """Hàm vẽ viền đỏ quanh quân vua khi bị chiếu"""
    row, col = king_position
    highlight_king = p.Surface((SQ_SIZE, SQ_SIZE))
    highlight_king.set_alpha(100)  # Độ trong suốt
    highlight_king.fill(p.Color('red'))  # Màu đỏ
    screen.blit(highlight_king, (col * SQ_SIZE, row * SQ_SIZE))

def highlight_squares(screen, game_state, square_selected):
    """Highlights square selected and last move made"""
    # Highlights selected square
    if square_selected != ():
        row, column = square_selected
        if game_state.board[row][column][0] == ('w' if game_state.white_to_move else 'b'):  # Clicks on own piece
            highlight_selected = p.Surface((SQ_SIZE, SQ_SIZE))
            highlight_selected.set_alpha(70)  # Transperancy value; 0 transparent; 255 opaque
            highlight_selected.fill(p.Color('blue'))
            screen.blit(highlight_selected, (column * SQ_SIZE, row * SQ_SIZE))

    # Highlights last move
    if len(game_state.move_log) != 0:
        last_move = game_state.move_log[-1]
        start_row, start_column = last_move.start_row, last_move.start_column
        end_row, end_column = last_move.end_row, last_move.end_column
        highlight_last = p.Surface((SQ_SIZE, SQ_SIZE))
        highlight_last.set_alpha(70)
        highlight_last.fill(p.Color('yellow'))
        screen.blit(highlight_last, (start_column * SQ_SIZE, start_row * SQ_SIZE))
        screen.blit(highlight_last, (end_column * SQ_SIZE, end_row * SQ_SIZE))

def highlight_valid_moves(screen, game_state, valid_moves, square_selected):
    """Vẽ các nước đi hợp lệ khi người chơi chọn một quân cờ"""
    for move in valid_moves:
        if move.start_row == square_selected[0] and move.start_column == square_selected[1]:
            highlight_moves = p.Surface((SQ_SIZE, SQ_SIZE), p.SRCALPHA)
            highlight_moves.set_alpha(100)  # Độ trong suốt
            p.draw.circle(highlight_moves, 'blue', (SQ_SIZE // 2, SQ_SIZE // 2), SQ_SIZE // 6)
            screen.blit(highlight_moves, (move.end_column * SQ_SIZE, move.end_row * SQ_SIZE))

def draw_move_log(screen, game_state):
    """Draws move log to the right of the screen"""
    move_log_area = p.Rect(SQ_SIZE * 8.1, SQ_SIZE * 2, SQ_SIZE * 4.4, SQ_SIZE * 7)
    p.draw.rect(screen, p.Color('grey22'), move_log_area)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = f'{i // 2 + 1}. {str(move_log[i])} '
        if i + 1 < len(move_log):  # Makes sure black has made a move
            move_string += f'{str(move_log[i + 1])} '
        move_texts.append(move_string)

    move_padding = 4
    text_y = move_padding
    for j in range(0, len(move_texts), 4):
        text_line = ' | '.join(move_texts[j:j + 4])
        text_object = small_font.render(text_line, True, p.Color('white'))
        text_location = move_log_area.move(move_padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height()

def animate_move(move, screen, board, clock):
    """Animates a move"""
    delta_row = move.end_row - move.start_row  # Change in row
    delta_column = move.end_column - move.start_column  # Change in column
    frames_per_square = 5  # Controls animation speed (frames to move one square)
    frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square

    for frame in range(frame_count + 1):  # Need +1 to complete the entire animation

        #  Frame/frame_count indicates how far along the action is
        row, column = (
            move.start_row + delta_row * frame / frame_count, move.start_column + delta_column * frame / frame_count)

        # Draw board and pieces for each frame of the animation
        draw_board(screen)
        draw_pieces(screen, board)

        # Erases the piece from its ending square
        colour = COLOR_A[(move.end_row + move.end_column) % 2]
        end_square = p.Rect(move.end_column * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, colour, end_square)

        # Draws a captured piece onto the rectangle if a piece is captured
        if move.piece_captured != '--':
            if move.is_en_passant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_column * SQ_SIZE, en_passant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(images[move.piece_captured], end_square)

        # Draws moving piece
        screen.blit(images[move.piece_moved], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        p.display.flip()
        clock.tick(60)  # Controls fame rate per second for the animation

def draw_button(text, x, y, color, hover_color):
    """Vẽ nút với màu sắc và vị trí đã chỉ định"""
    mouse_pos = p.mouse.get_pos()
    button_rect = p.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    if button_rect.collidepoint(mouse_pos):
        p.draw.rect(screen, hover_color, button_rect)
    else:
        p.draw.rect(screen, color, button_rect)

    text_surface = large_font.render(text, True, 'black')
    screen.blit(text_surface, text_surface.get_rect(center=button_rect.center))
    return button_rect

def draw_button(text, x, y, color, hover_color):
    """Vẽ nút với màu sắc và vị trí đã chỉ định"""
    mouse_pos = p.mouse.get_pos()
    button_rect = p.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    if button_rect.collidepoint(mouse_pos):
        p.draw.rect(screen, hover_color, button_rect)
    else:
        p.draw.rect(screen, color, button_rect)

    text_surface = large_font.render(text, True, 'black')
    screen.blit(text_surface, text_surface.get_rect(center=button_rect.center))
    return button_rect

def draw_endgame_text(screen, text):
    """Vẽ văn bản khi kết thúc trò chơi"""
    text_object = large_font.render(text, True, p.Color('white'))
    text_location = p.Rect(SQ_SIZE * 8.43, SQ_SIZE // 1.75, 0, 0)
    screen.blit(text_object, text_location)