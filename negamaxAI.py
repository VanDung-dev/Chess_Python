import random

# Độ sâu của thuật toán xác định AI di chuyển. Set_depth cao hơn == AI khó hơn. Thấp hơn nếu động cơ quá chậm.
# set_depth = 4

# Giá trị tích cực là tốt cho màu trắng, tiêu cực cho màu đen. Tức là Checkmate đen = -1000
checkmate_points = 1000
stalemate_points = 0

piece_scores = {'K': 200.0, 'Q': 9.0, 'R': 5.0, 'B': 3.3, 'N': 3.2, 'P': 1.0}
piece_positions = {
    'wP': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'bP': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'wN': [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 5.0, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 5.0, -3.0],
        [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]],
    'bN': [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]],
    'wB': [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]],
    'bB': [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]],
    'wR': [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]],
    'bR': [
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    'wQ': [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]],
    "bQ": [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]],
    'wK': [  # Uses chessprogramming.org King middle game values
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]],
    'bK': [  # Uses chessprogramming.org King middle game values
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]]}

def find_random_move(valid_moves):
    return random.choice(valid_moves)

def find_best_move(game_state, valid_moves, SQ_SIZE, depth):
    """Phương pháp trợ giúp để thực hiện cuộc gọi đệ quy đầu tiên"""
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    find_negamax_move_alphabeta(game_state, valid_moves, depth, -checkmate_points, checkmate_points,
                                        1 if game_state.white_to_move else -1, SQ_SIZE, depth)
    return next_move


def find_negamax_move_alphabeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier, SQ_SIZE, set_depth):
    """
    Thuật toán Negamax với cắt tỉa alpha beta.

    Alpha Beta cắt tỉa loại bỏ sự cần thiết phải kiểm tra tất cả các động tác trong cây game_state khi
    Một chi nhánh tốt hơn đã được tìm thấy hoặc một nhánh có điểm quá thấp.

    alpha: giới hạn trên (tối đa có thể); Beta: giới hạn dưới (tối thiểu có thể)
    Nếu điểm tối đa lớn hơn alpha, điều đó sẽ trở thành giá trị alpha mới.
    Nếu alpha trở thành> = beta, thoát ra khỏi nhánh.

    Màu trắng luôn cố gắng tối đa hóa điểm số và màu đen luôn
    Cố gắng giảm thiểu điểm số. Một khi khả năng tối đa hoặc thấp hơn tối đa
    đã bị loại bỏ, không cần phải kiểm tra thêm các nhánh.
    """
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_state)

    max_score = -checkmate_points
    random.shuffle(valid_moves)

    for move in valid_moves:
        game_state.make_move(move, SQ_SIZE)
        next_moves = game_state.get_valid_moves()
        score = -find_negamax_move_alphabeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier, SQ_SIZE, set_depth)

        if score > max_score:
            max_score = score
            if depth == set_depth:
                next_move = move
        game_state.undo_move()

        # Pruning
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


def score_board(game_state):
    """Điểm tích cực là tốt cho màu trắng; Điểm âm là tốt cho màu đen."""
    if game_state.checkmate:
        if game_state.white_to_move:
            return -checkmate_points  # Black wins
        else:
            return checkmate_points  # White wins
    elif game_state.stalemate:
        return stalemate_points

    score = 0
    for row in range(len(game_state.board)):
        for column in range(len(game_state.board)):
            if game_state.board[row][column][0] == 'w':
                score += piece_scores[game_state.board[row][column][1]]
                score += piece_positions[game_state.board[row][column]][row][column]
            elif game_state.board[row][column][0] == 'b':
                score -= piece_scores[game_state.board[row][column][1]]
                score -= piece_positions[game_state.board[row][column]][row][column]
    return score
