document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const resetBtn = document.querySelector('.restart-btn');
    const status = document.querySelector('.status-message');
    const winLine = document.querySelector('#win-line');
    let gameActive = true;
    let board = initializeBoard();

    cells.forEach(cell => cell.addEventListener('click', handleMove));
    resetBtn.addEventListener('click', resetGame);

    async function handleMove(e) {
        if (!gameActive) return;
        
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        
        if (board[row][col] !== ' ') return;

        try {
            const response = await fetch('/move', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ board, row, col })
            });
            
            const data = await response.json();
            
            if (data.error) {
                showError(data.error);
                return;
            }

            board = data.board;
            updateUI();

            if (data.winner || data.draw) {
                endGame(data.winner, data.draw, data.winning_cells);
                return;
            }

            if (data.ai_move) {
                const [aiRow, aiCol] = data.ai_move;
                board[aiRow][aiCol] = 'X';
                updateUI();
            }

            if (data.winner || data.draw) {
                endGame(data.winner, data.draw, data.winning_cells);
            }
        } catch (error) {
            showError('Error making move');
            console.error('Error:', error);
        }
    }

    function updateUI() {
        cells.forEach(cell => {
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            cell.textContent = board[row][col];
            cell.className = `cell ${board[row][col].toLowerCase()}`;
        });
    }

    function endGame(winner, draw, winningCells) {
        gameActive = false;
        if (winner) {
            status.textContent = `${winner} wins!`;
            drawWinLine(winningCells);
        } else if (draw) {
            status.textContent = "It's a draw!";
        }
    }

    function drawWinLine(winningCells) {
        if (!winningCells) return;
        
        const firstCell = document.querySelector(`[data-row="${winningCells[0][0]}"][data-col="${winningCells[0][1]}"]`);
        const lastCell = document.querySelector(`[data-row="${winningCells[2][0]}"][data-col="${winningCells[2][1]}"]`);
        
        const boardRect = document.querySelector('.game-board').getBoundingClientRect();
        const firstRect = firstCell.getBoundingClientRect();
        const lastRect = lastCell.getBoundingClientRect();
        
        const centerX1 = firstRect.left + firstRect.width/2 - boardRect.left;
        const centerY1 = firstRect.top + firstRect.height/2 - boardRect.top;
        const centerX2 = lastRect.left + lastRect.width/2 - boardRect.left;
        const centerY2 = lastRect.top + lastRect.height/2 - boardRect.top;
        
        const length = Math.sqrt(Math.pow(centerX2 - centerX1, 2) + Math.pow(centerY2 - centerY1, 2));
        const angle = Math.atan2(centerY2 - centerY1, centerX2 - centerX1);
        
        winLine.style.width = `${length}px`;
        winLine.style.left = `${centerX1}px`;
        winLine.style.top = `${centerY1}px`;
        winLine.style.transform = `rotate(${angle}rad)`;
        winLine.style.display = 'block';
    }

    async function resetGame() {
        try {
            const response = await fetch('/reset');
            const data = await response.json();
            board = data.board;
            gameActive = true;
            status.textContent = '';
            winLine.style.display = 'none';
            updateUI();
            cells.forEach(cell => cell.classList.remove('x', 'o'));
        } catch (error) {
            showError('Error resetting game');
            console.error('Error:', error);
        }
    }

    function showError(message) {
        status.textContent = message;
        setTimeout(() => status.textContent = '', 3000);
    }

    function initializeBoard() {
        return [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ];
    }
});