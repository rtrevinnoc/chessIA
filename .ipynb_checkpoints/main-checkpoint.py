import chess
import random

# Define the maximum search depth
MAX_DEPTH = 3

# Evaluation function to determine the value of the board state
def evaluate_board(board):
    piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                score += piece_values[piece.symbol().upper()]
            else:
                score -= piece_values[piece.symbol().upper()]
    return score

# Minimax function to search for the best move
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if maximizing_player:
        max_eval = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to make the AI move
def make_move(board):
    best_move = None
    best_eval = float("-inf")
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, MAX_DEPTH, float("-inf"), float("inf"), False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move

if input("Color para IA? ") == "B":
    print("IA es color Blanco")
    enemy = chess.BLACK
else:
    print("IA es color Negro")
    enemy = chess.WHITE

# Play the game
board = chess.Board()
while not board.is_game_over():
    if board.turn == enemy:
        move = input("\nIntroduce un movimiento (notacion algebraica): ")
        # try:
        board.push_san(move)
        # except ValueError:
        #     print("\n# ERROR: Movimiento Invalido.\n\n")
    else:
        print("\nCalculando un movimiento.")
        move = make_move(board)
        board.push(move)
        print(f"IA realiza el movimiento {move}\n")
    print(board.unicode(borders=True))
print("Resultado: ", board.result())
