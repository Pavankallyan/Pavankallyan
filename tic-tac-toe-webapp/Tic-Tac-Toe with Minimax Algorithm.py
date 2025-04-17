import math

# Initialize the Tic-Tac-Toe board
def initialize_board():
    """
    Initializes the Tic-Tac-Toe board as a 3x3 grid filled with empty spaces.

    Returns:
        list: A 3x3 list representing the game board.
    """
    return [[" " for _ in range(3)] for _ in range(3)]

# Display the current state of the board
def display_board(board):
    """
    Displays the current state of the Tic-Tac-Toe board.

    Args:
        board (list): The 3x3 game board.
    """
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Check if a move is valid
def is_valid_move(board, row, col):
    """
    Checks if a move is valid (i.e., the cell is empty).

    Args:
        board (list): The 3x3 game board.
        row (int): The row index of the move.
        col (int): The column index of the move.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    return board[row][col] == " "

# Make a move on the board
def make_move(board, row, col, player):
    """
    Makes a move on the board for the given player.

    Args:
        board (list): The 3x3 game board.
        row (int): The row index of the move.
        col (int): The column index of the move.
        player (str): The player making the move ("X" or "O").

    Returns:
        bool: True if the move was successful, False otherwise.
    """
    if is_valid_move(board, row, col):
        board[row][col] = player
        return True
    return False

# Check if there is a winner
def check_winner(board):
    """
    Checks if there is a winner on the board.

    Args:
        board (list): The 3x3 game board.

    Returns:
        str: The winning player ("X" or "O"), or None if there is no winner.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    
    return None

# Check if the game is a draw
def is_draw(board):
    """
    Checks if the game is a draw (i.e., the board is full and there is no winner).

    Args:
        board (list): The 3x3 game board.

    Returns:
        bool: True if the game is a draw, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True

# Minimax algorithm with Alpha-Beta Pruning
def minimax_with_alpha_beta(board, depth, is_maximizing, alpha, beta):
    """
    Implements the Minimax algorithm with Alpha-Beta Pruning.

    Args:
        board (list): The current state of the game board.
        depth (int): The depth of the recursion (used for optimization).
        is_maximizing (bool): True if the current player is maximizing, False if minimizing.
        alpha (float): The best score that the maximizing player can guarantee.
        beta (float): The best score that the minimizing player can guarantee.

    Returns:
        int: The score of the board state.
    """
    # Check for terminal states
    winner = check_winner(board)
    if winner == "X":  # AI wins
        return 1
    elif winner == "O":  # Human wins
        return -1
    elif is_draw(board):  # Draw
        return 0

    # Maximizing player's turn (AI)
    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"  # AI makes a move
                    score = minimax_with_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][col] = " "  # Undo the move
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)  # Update alpha
                    if beta <= alpha:  # Prune the branch
                        break
        return best_score

    # Minimizing player's turn (Human)
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"  # Human makes a move
                    score = minimax_with_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][col] = " "  # Undo the move
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)  # Update beta
                    if beta <= alpha:  # Prune the branch
                        break
        return best_score

# Find the best move for the AI
def find_best_move_with_alpha_beta(board):
    """
    Finds the best move for the AI using the Minimax algorithm with Alpha-Beta Pruning.

    Args:
        board (list): The current state of the game board.

    Returns:
        tuple: The row and column of the best move.
    """
    best_score = -math.inf
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "X"  # AI makes a move
                score = minimax_with_alpha_beta(board, 0, False, -math.inf, math.inf)
                board[row][col] = " "  # Undo the move
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move

# Main function to play the game
def play_game_with_ai():
    """
    Main function to play the Tic-Tac-Toe game with an AI opponent.
    The AI uses the Minimax algorithm to make optimal moves.
    """
    board = initialize_board()
    current_player = "O"  # Human starts first

    while True:
        display_board(board)

        if current_player == "X":
            print("AI's turn (X).")
            row, col = find_best_move_with_alpha_beta(board)  # AI calculates the best move
            make_move(board, row, col, "X")
        else:
            print("Your turn (O).")
            while True:
                try:
                    user_input = input("Enter row and column (0-2) separated by space: ")
                    row, col = map(int, user_input.split())
                    if row < 0 or row > 2 or col < 0 or col > 2:
                        print("Invalid input. Row and column must be between 0 and 2.")
                        continue
                    if not make_move(board, row, col, "O"):
                        print("Invalid move. The cell is already occupied. Try again.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter two numbers between 0 and 2 separated by a space.")

        # Check for a winner
        winner = check_winner(board)
        if winner:
            display_board(board)
            print(f"Player {winner} wins!")
            break

        # Check for a draw
        if is_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        # Switch player
        current_player = "O" if current_player == "X" else "X"

# Run the game with AI
if __name__ == "__main__":
    play_game_with_ai()