import chess, math, time

MAX_DEPTH = 3

# Calcular estructura de los peones, si estan solos
def is_isolated_pawn(board, square):
    file = chess.square_file(square)
    adjacent_files = [file - 1, file + 1]
    for adj_file in adjacent_files:
        if adj_file < 0 or adj_file > 7:
            continue
        adj_square = chess.square(adj_file, chess.square_rank(square))
        if board.piece_at(adj_square) == chess.Piece(chess.PAWN, board.turn):
            return False
    return True

piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}

# Calcular piezas restantes
def material_advantage(board, color):
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == color:
                score += piece_values[piece.piece_type]
            else:
                score -= piece_values[piece.piece_type]
    return score

# Calcular valor del tablero mediante la estructura de los peones y el numero de piezas restantes
def evaluate_board(board):
    material_advantage_score = (material_advantage(board, ia) - material_advantage(board, enemy))

    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    white_pawn_structure = sum(1 for square in white_pawns if is_isolated_pawn(board, square))
    black_pawn_structure = sum(1 for square in black_pawns if is_isolated_pawn(board, square))
    pawn_structure_advantage = white_pawn_structure - black_pawn_structure

    return (
        material_advantage_score * 0.75
        + pawn_structure_advantage * 0.25
    )

# Buscar mejor movimiento con Minimax de poda alfa-beta
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if maximizing_player:
        max_eval = -math.inf
        for move in board.legal_moves:
            board.push(move)
            val = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in board.legal_moves:
            board.push(move)
            val = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval

# Generar un movimiento con Minimax
def make_move(board):
    best_move = None
    best_eval = -math.inf
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, MAX_DEPTH, -math.inf, math.inf, False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

def get_all_pieces_by_color(board, color):
    pieces = []
    for piece_type in chess.PIECE_TYPES:
        pieces.extend(board.pieces(piece_type, color))
    return len(pieces)

def update_piece_movements(board: chess.Board, move: chess.Move, moves_dict):
    piece_type = board.piece_at(move.to_square).piece_type
    moves_dict[piece_type] = moves_dict[piece_type] + 1

def update_movements(board: chess.Board, moves_list: list, movement: str):
    if board.is_checkmate() or board.is_stalemate():
        moves_list.append("#" + movement)
    elif board.is_check():
        moves_list.append("+" + movement)
    else:
        moves_list.append(movement)

if input("Color para IA? ").lower().startswith("b"):
    print("IA es color Blanco")
    enemy = chess.BLACK
    ia = chess.WHITE;
else:
    print("IA es color Negro")
    enemy = chess.WHITE
    ia = chess.BLACK

board = chess.Board()

ia_moves = []
human_moves = []

ia_pieces = []
human_pieces = []

ia_times = []
human_times = []

ia_piece_moves = {chess.PAWN: 0, chess.KNIGHT: 0, chess.BISHOP: 0, chess.ROOK: 0, chess.QUEEN: 0, chess.KING: 0}
human_piece_moves = {chess.PAWN: 0, chess.KNIGHT: 0, chess.BISHOP: 0, chess.ROOK: 0, chess.QUEEN: 0, chess.KING: 0}

print(board.unicode(borders=True, invert_color=True))

while not board.is_game_over():
    if board.turn == enemy:
        start = time.time()
        move = input("\nIntroduce un movimiento: ")
        end = time.time()
        human_times.append(end - start)
        try:
            board.push_san(move)
            print(f"Realizaste el movimiento {move.upper()}\n")
            update_movements(board, human_moves, move.upper())
            human_pieces.append(get_all_pieces_by_color(board, enemy))
            update_piece_movements(board, chess.Move.from_uci(move), human_piece_moves)
        except ValueError:
            print("\n# ERROR: Movimiento Invalido.\n\n")
    else:
        print("\nCalculando un movimiento.")
        start = time.time()
        move = make_move(board)
        end = time.time()
        ia_times.append(end - start)
        board.push(move)
        print(f"IA realiza el movimiento {move.uci().upper()}\n")
        update_movements(board, ia_moves, move.uci().upper())
        ia_pieces.append(get_all_pieces_by_color(board, ia))
        update_piece_movements(board, move, ia_piece_moves)

    print("###################### IA STATS #######################")
    print("#MOVES=> ", ia_moves)
    print("#TIMES=> ", ia_times)
    print("#PIECES=> ", ia_pieces)
    print("#MOV/PIECE=> ", ia_piece_moves)
    print("####################################################")
    print("###################### HUMAN STATS #######################")
    print("#MOVES=> ", human_moves)
    print("#TIMES=> ", human_times)
    print("#PIECES=> ", human_pieces)
    print("#MOV/PIECE=> ", human_piece_moves)
    print("####################################################")

    print(board.unicode(borders=True, invert_color=True))
print("Resultado: ", board.result())

print("\n\n###################### IA STATS #######################")
print("#MOVES=> ", ia_moves)
print("#TIMES=> ", ia_times)
print("#PIECES=> ", ia_pieces)
print("#MOV/PIECE=> ", ia_piece_moves)
print("####################################################")
print("###################### HUMAN STATS #######################")
print("#MOVES=> ", human_moves)
print("#TIMES=> ", human_times)
print("#PIECES=> ", human_pieces)
print("#MOV/PIECE=> ", human_piece_moves)
print("####################################################")
