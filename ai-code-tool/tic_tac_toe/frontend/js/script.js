/* script.js */

const board = document.getElementById('board');
const cells = [];
let currentPlayer = null; // 'X' or 'O'
let gameBoard = ['', '', '', '', '', '', '', '', '']; // Game state

// Connect to WebSocket server
const socket = new WebSocket('ws://localhost:8080');

// Handle incoming WebSocket messages
socket.onmessage = function (event) {
  const message = JSON.parse(event.data);

  if (message.type === 'start') {
    currentPlayer = message.player;
    alert(`${currentPlayer}'s turn!`);
  }

  if (message.type === 'move') {
    const { index, player } = message;
    gameBoard[index] = player;
    updateBoard();
  }

  if (message.type === 'win') {
    alert(`${message.player} wins!`);
    resetBoard();
  }
};

// Dynamically create the 3x3 grid of cells
for (let i = 0; i < 9; i++) {
  const cell = document.createElement('div');
  cell.classList.add('cell');
  cell.addEventListener('click', () => handleCellClick(i));
  board.appendChild(cell);
  cells.push(cell);
}

function handleCellClick(index) {
  if (gameBoard[index] !== '') return; // Don't allow a move in a filled cell
  if (currentPlayer === null) return; // Wait for both players to join

  gameBoard[index] = currentPlayer;
  cells[index].textContent = currentPlayer;

  // Send the move to the server
  socket.send(JSON.stringify({ type: 'move', index, player: currentPlayer }));

  if (checkWin()) {
    socket.send(JSON.stringify({ type: 'win', player: currentPlayer }));
  } else {
    // Switch player
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    alert(`${currentPlayer}'s turn!`);
  }
}

function checkWin() {
  const winningCombinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];

  for (const combination of winningCombinations) {
    const [a, b, c] = combination;
    if (gameBoard[a] && gameBoard[a] === gameBoard[b] && gameBoard[a] === gameBoard[c]) {
      return true;
    }
  }
  return false;
}

function updateBoard() {
  gameBoard.forEach((value, index) => {
    cells[index].textContent = value;
  });
}

function resetBoard() {
  gameBoard = ['', '', '', '', '', '', '', '', ''];
  updateBoard();
  currentPlayer = null;
}