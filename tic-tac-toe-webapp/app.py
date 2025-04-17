from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return {'winner': board[i][0], 'cells': [[i,0], [i,1], [i,2]]}
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return {'winner': board[0][i], 'cells': [[0,i], [1,i], [2,i]]}
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return {'winner': board[0][0], 'cells': [[0,0], [1,1], [2,2]]}
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return {'winner': board[0][2], 'cells': [[0,2], [1,1], [2,0]]}
    return None

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def minimax_with_alpha_beta(board, depth, is_maximizing, alpha, beta):
    result = check_winner(board)
    if result: return 1 if result['winner'] == "X" else -1
    if is_draw(board): return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax_with_alpha_beta(board, depth+1, False, alpha, beta)
                    board[row][col] = " "
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha: break
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax_with_alpha_beta(board, depth+1, True, alpha, beta)
                    board[row][col] = " "
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha: break
        return best_score

def find_best_move(board):
    best_score = -math.inf
    best_move = (-1, -1)
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "X"
                score = minimax_with_alpha_beta(board, 0, False, -math.inf, math.inf)
                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        board = data['board']
        row, col = data['row'], data['col']
        
        if board[row][col] != " ": return jsonify({"error": "Invalid move"}), 400
        
        board[row][col] = "O"
        winner_info = check_winner(board)
        if winner_info or is_draw(board):
            return jsonify({
                "board": board,
                "winner": winner_info['winner'] if winner_info else None,
                "winning_cells": winner_info['cells'] if winner_info else None,
                "draw": is_draw(board)
            })
        
        ai_row, ai_col = find_best_move(board)
        board[ai_row][ai_col] = "X"
        winner_info = check_winner(board)
        return jsonify({
            "board": board,
            "ai_move": (ai_row, ai_col),
            "winner": winner_info['winner'] if winner_info else None,
            "winning_cells": winner_info['cells'] if winner_info else None,
            "draw": is_draw(board)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset')
def reset():
    return jsonify({"board": initialize_board()})

if __name__ == '__main__':
    app.run(debug=True)