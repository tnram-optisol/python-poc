value = {
  "frontend": {
    "html": {
      "index.html": {
        "code": "<!-- index.html -->\n<!DOCTYPE html>\n<html>\n<head>\n  <title>Tic Tac Toe</title>\n  <link rel=\"stylesheet\" href=\"styles.css\">\n</head>\n<body>\n  <h1>Tic Tac Toe</h1>\n  <div id=\"board\">\n    <!-- Game board will be dynamically generated here -->\n  </div>\n  <script src=\"script.js\"></script>\n</body>\n</html>"
      }
    },
    "css": {
      "styles.css": {
        "code": "/* styles.css */\n#board {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-gap: 10px;\n  width: 300px;\n  margin: 0 auto;\n}\n\n.cell {\n  height: 100px;\n  border: 1px solid black;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  font-size: 24px;\n  cursor: pointer;\n}"
      }
    },
    "js": {
      "script.js": {
        "code": "/* script.js */\nconst board = document.getElementById('board');\nconst cells = Array.from(board.getElementsByTagName('div'));\nlet currentPlayer = 'X';\n\ncells.forEach((cell) => {\n  cell.addEventListener('click', handleCellClick);\n});\n\nfunction handleCellClick(event) {\n  const cell = event.target;\n  if (cell.textContent !== '') return;\n  cell.textContent = currentPlayer;\n  if (checkWin()) {\n    alert(`${currentPlayer} wins!`);\n    resetBoard();\n  } else {\n    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';\n  }\n}\n\nfunction checkWin() {\n  const winningCombinations = [\n    [0, 1, 2],\n    [3, 4, 5],\n    [6, 7, 8],\n    [0, 3, 6],\n    [1, 4, 7],\n    [2, 5, 8],\n    [0, 4, 8],\n    [2, 4, 6]\n  ];\n  for (const combination of winningCombinations) {\n    const [a, b, c] = combination;\n    if (\n      cells[a].textContent === currentPlayer &&\n      cells[b].textContent === currentPlayer &&\n      cells[c].textContent === currentPlayer\n    ) {\n      return true;\n    }\n  }\n  return false;\n}\n\nfunction resetBoard() {\n  cells.forEach((cell) => {\n    cell.textContent = '';\n  });\n  currentPlayer = 'X';\n}"
      }
    }
  },
  "backend": {
    "js": {
      "server.js": {
        "code": "/* server.js */\nconst express = require('express');\nconst app = express();\nconst port = 3000;\n\napp.use(express.static('public'));\n\napp.listen(port, () => {\n  console.log(`Server is running at http://localhost:${port}`);\n});"
      }
    }
  }
}