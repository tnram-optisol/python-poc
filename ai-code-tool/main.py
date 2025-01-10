# Retry creating the TypeScript project zip for the user

import os
from os.path import exists
from zipfile import ZipFile

# Redefine project structure for TypeScript
# frontend_ts_files = {
#   "frontend/public/index.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>Todo List</title>\n</head>\n<body>\n  <div id=\"root\"></div>\n</body>\n</html>",
#
#   "frontend/src/index.tsx": "import React from 'react';\nimport ReactDOM from 'react-dom';\nimport './styles.css';\nimport App from './App';\nimport { Provider } from 'react-redux';\nimport store from './redux/store';\n\nReactDOM.render(\n  <Provider store={store}>\n    <App />\n  </Provider>,\n  document.getElementById('root')\n);",
#
#   "frontend/src/App.tsx": "import React from 'react';\nimport TodoList from './components/TodoList';\n\nfunction App() {\n  return (\n    <div>\n      <h1>Todo List</h1>\n      <TodoList />\n    </div>\n  );\n}\n\nexport default App;",
#
#   "frontend/src/components/TodoList.tsx": "import React, { useState, useEffect } from 'react';\nimport { useDispatch, useSelector } from 'react-redux';\nimport { fetchTodos, createTodo, removeTodo } from '../redux/actions/todoActions';\nimport TodoItem from './TodoItem';\n\ninterface Todo {\n  _id: string;\n  text: string;\n}\n\nconst TodoList: React.FC = () => {\n  const [newTodo, setNewTodo] = useState<string>('');\n  const dispatch = useDispatch();\n  const todos = useSelector((state: any) => state.todos);\n\n  useEffect(() => {\n    dispatch(fetchTodos());\n  }, [dispatch]);\n\n  const addTodo = () => {\n    if (newTodo.trim()) {\n      dispatch(createTodo(newTodo));\n      setNewTodo('');\n    }\n  };\n\n  const deleteTodo = (id: string) => {\n    dispatch(removeTodo(id));\n  };\n\n  return (\n    <div className=\"todo-container\">\n      <div className=\"todo-input\">\n        <input\n          type=\"text\"\n          value={newTodo}\n          onChange={(e) => setNewTodo(e.target.value)}\n          placeholder=\"Enter a new todo\"\n        />\n        <button onClick={addTodo}>Add Todo</button>\n      </div>\n\n      <ul className=\"todo-list\">\n        {todos.map((todo: Todo) => (\n          <TodoItem key={todo._id} todo={todo} onDelete={deleteTodo} />\n        ))}\n      </ul>\n    </div>\n  );\n};\n\nexport default TodoList;",
#
#   "frontend/src/components/TodoItem.tsx": "import React from 'react';\n\ninterface Todo {\n  text: string;\n  _id: string;\n}\n\ninterface TodoItemProps {\n  todo: Todo;\n  onDelete: (id: string) => void;\n}\n\nconst TodoItem: React.FC<TodoItemProps> = ({ todo, onDelete }) => {\n  return (\n    <li className=\"todo-item\">\n      {todo.text}\n      <button onClick={() => onDelete(todo._id)}>Delete</button>\n    </li>\n  );\n};\n\nexport default TodoItem;",
#
#   "frontend/src/styles.css": "body {\n  font-family: 'Arial', sans-serif;\n  margin: 0;\n  padding: 0;\n  background-color: #f4f4f4;\n}\n\n.todo-container {\n  width: 100%;\n  max-width: 600px;\n  margin: 0 auto;\n  padding: 20px;\n  background-color: white;\n  border-radius: 8px;\n  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);\n}\n\n.todo-input {\n  display: flex;\n  justify-content: space-between;\n  margin-bottom: 20px;\n}\n\n.todo-input input {\n  width: 80%;\n  padding: 10px;\n  font-size: 1rem;\n  border: 1px solid #ccc;\n  border-radius: 4px;\n}\n\n.todo-input button {\n  padding: 10px 15px;\n  font-size: 1rem;\n  background-color: #4CAF50;\n  color: white;\n  border: none;\n  border-radius: 4px;\n  cursor: pointer;\n}\n\n.todo-input button:hover {\n  background-color: #45a049;\n}\n\n.todo-list {\n  list-style-type: none;\n  padding: 0;\n}\n\n.todo-item {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: 12px;\n  border-bottom: 1px solid #eee;\n  font-size: 1.1rem;\n}\n\n.todo-item button {\n  background-color: #f44336;\n  color: white;\n  border: none;\n  border-radius: 4px;\n  cursor: pointer;\n}\n\n.todo-item button:hover {\n  background-color: #e53935;\n}\n\n/* Responsive Styles */\n@media (max-width: 600px) {\n  .todo-container {\n    padding: 10px;\n  }\n\n  .todo-input input {\n    width: 70%;\n  }\n}",
#
#   "frontend/redux/actions/todoActions.ts": "import { Dispatch } from 'redux';\n\ninterface Todo {\n  _id: string;\n  text: string;\n}\n\n// Action Types\nconst SET_TODOS = 'SET_TODOS';\nconst ADD_TODO = 'ADD_TODO';\nconst DELETE_TODO = 'DELETE_TODO';\n\n// Action Creators\nconst setTodos = (todos: Todo[]) => ({\n  type: SET_TODOS,\n  payload: todos,\n});\n\nconst addTodo = (todo: Todo) => ({\n  type: ADD_TODO,\n  payload: todo,\n});\n\nconst deleteTodo = (id: string) => ({\n  type: DELETE_TODO,\n  payload: id,\n});\n\n// Thunk actions\nexport const fetchTodos = () => {\n  return async (dispatch: Dispatch) => {\n    const res = await fetch('/api/todos');\n    const data = await res.json();\n    dispatch(setTodos(data));\n  };\n};\n\nexport const createTodo = (text: string) => {\n  return async (dispatch: Dispatch) => {\n    const res = await fetch('/api/todos', {\n      method: 'POST',\n      headers: { 'Content-Type': 'application/json' },\n      body: JSON.stringify({ text }),\n    });\n    const newTodo = await res.json();\n    dispatch(addTodo(newTodo));\n  };\n};\n\nexport const removeTodo = (id: string) => {\n  return async (dispatch: Dispatch) => {\n    await fetch(`/api/todos/${id}`, { method: 'DELETE' });\n    dispatch(deleteTodo(id));\n  };\n};",
#
#   "frontend/redux/reducers/todoReducer.ts": "import { SET_TODOS, ADD_TODO, DELETE_TODO } from '../actions/todoActions';\n\ninterface Todo {\n  _id: string;\n  text: string;\n}\n\ninterface TodoState {\n  todos: Todo[];\n}\n\nconst initialState: TodoState = {\n  todos: [],\n};\n\nconst todoReducer = (state = initialState, action: any): TodoState => {\n  switch (action.type) {\n    case SET_TODOS:\n      return { ...state, todos: action.payload };\n    case ADD_TODO:\n      return { ...state, todos: [...state.todos, action.payload] };\n    case DELETE_TODO:\n      return { ...state, todos: state.todos.filter((todo) => todo._id !== action.payload) };\n    default:\n      return state;\n  }\n};\n\nexport default todoReducer;",
#
#   "frontend/redux/store.ts": "import { createStore, applyMiddleware } from 'redux';\nimport thunk from 'redux-thunk';\nimport todoReducer from './reducers/todoReducer';\n\nconst store = createStore(todoReducer, applyMiddleware(thunk));\n\nexport default store;",
#
#   "frontend/package.json": "{\n  \"name\": \"frontend\",\n  \"version\": \"1.0.0\",\n  \"main\": \"index.tsx\",\n  \"dependencies\": {\n    \"react\": \"^18.2.0\",\n    \"react-dom\": \"^18.2.0\",\n    \"redux\": \"^4.2.2\",\n    \"react-redux\": \"^8.0.0\",\n    \"redux-thunk\": \"^2.4.2\",\n    \"typescript\": \"^4.4.4\"\n  },\n  \"scripts\": {\n    \"start\": \"react-scripts start\",\n    \"build\": \"react-scripts build\",\n    \"test\": \"react-scripts test\",\n    \"eject\": \"react-scripts eject\"\n  },\n  \"devDependencies\": {\n    \"@types/react\": \"^18.0.0\",\n    \"@types/react-dom\": \"^18.0.0\",\n    \"react-scripts\": \"4.0.3\"\n  }\n}"
# }
#
# backend_ts_files = {
#   "backend/app.ts": "import express from 'express';\nimport cors from 'cors';\nimport { connectDB } from './config/db';\nimport todoRoutes from './routes';\n\nconst app = express();\nconnectDB();\n\napp.use(cors());\napp.use(express.json());\n\napp.use('/api/todos', todoRoutes);\n\nconst PORT = process.env.PORT || 5000;\napp.listen(PORT, () => {\n  console.log(`Server running on port ${PORT}`);\n});",
#
#   "backend/config/db.ts": "import mongoose from 'mongoose';\n\nexport const connectDB = async () => {\n  try {\n    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/todolist', {\n      useNewUrlParser: true,\n      useUnifiedTopology: true,\n    });\n    console.log('MongoDB connected');\n  } catch (error) {\n    console.error('Database connection failed:', error);\n    process.exit(1);\n  }\n};",
#
#   "backend/models.ts": "import mongoose, { Schema, Document } from 'mongoose';\n\ninterface ITodo extends Document {\n  text: string;\n}\n\nconst TodoSchema: Schema = new Schema({\n  text: {\n    type: String,\n    required: true,\n  },\n});\n\nconst Todo = mongoose.model<ITodo>('Todo', TodoSchema);\n\nexport default Todo;",
#
#   "backend/validators/todoValidator.ts": "import Joi from 'joi';\n\n// Define the validation schema for the Todo model\nexport const todoValidationSchema = Joi.object({\n  text: Joi.string().min(1).required().messages({\n    'string.base': '\"text\" should be a type of \"text\"',\n    'string.empty': '\"text\" cannot be an empty field',\n    'any.required': '\"text\" is a required field',\n  }),\n});",
#
#   "backend/controllers/todoController.ts": "import { Request, Response } from 'express';\nimport * as todoService from '../services/todoService';\nimport { todoValidationSchema } from '../validators/todoValidator';\nimport Joi from 'joi';\n\n// Get all todos\nexport const getAllTodos = async (req: Request, res: Response) => {\n  try {\n    const todos = await todoService.getAllTodos();\n    res.json(todos);\n  } catch (err) {\n    res.status(500).json({ message: 'Server error', error: err.message });\n  }\n};\n\n// Get todo by ID\nexport const getTodoById = async (req: Request, res: Response) => {\n  const { id } = req.params;\n  try {\n    const todo = await todoService.getTodoById(id);\n    if (!todo) {\n      return res.status(404).json({ message: 'Todo not found' });\n    }\n    res.json(todo);\n  } catch (err) {\n    res.status(500).json({ message: 'Server error', error: err.message });\n  }\n};\n\n// Add a new todo\nexport const addTodo = async (req: Request, res: Response) => {\n  const { text } = req.body;\n\n  // Validate the request body\n  const { error } = todoValidationSchema.validate({ text });\n  if (error) {\n    return res.status(400).json({\n      message: 'Validation error',\n      details: error.details,\n    });\n  }\n\n  try {\n    const newTodo = await todoService.addTodo(text);\n    res.json(newTodo);\n  } catch (err) {\n    res.status(500).json({ message: 'Server error', error: err.message });\n  }\n};\n\n// Update an existing todo\nexport const updateTodo = async (req: Request, res: Response) => {\n  const { id } = req.params;\n  const { text } = req.body;\n\n  // Validate the request body\n  const { error } = todoValidationSchema.validate({ text });\n  if (error) {\n    return res.status(400).json({\n      message: 'Validation error',\n      details: error.details,\n    });\n  }\n\n  try {\n    const updatedTodo = await todoService.updateTodo(id, text);\n    if (!updatedTodo) {\n      return res.status(404).json({ message: 'Todo not found' });\n    }\n    res.json(updatedTodo);\n  } catch (err) {\n    res.status(500).json({ message: 'Server error', error: err.message });\n  }\n};\n\n// Delete a todo\nexport const deleteTodo = async (req: Request, res: Response) => {\n  const { id } = req.params;\n  try {\n    const deletedTodo = await todoService.deleteTodo(id);\n    if (!deletedTodo) {\n      return res.status(404).json({ message: 'Todo not found' });\n    }\n    res.json({ message: 'Todo deleted successfully' });\n  } catch (err) {\n    res.status(500).json({ message: 'Server error', error: err.message });\n  }\n};",
#
#   "backend/services/todoService.ts": "import Todo from '../models';\n\n// Get all todos\nexport const getAllTodos = async () => {\n  return await Todo.find();\n};\n\n// Get a single todo by ID\nexport const getTodoById = async (id: string) => {\n  return await Todo.findById(id);\n};\n\n// Add a new todo\nexport const addTodo = async (text: string) => {\n  const newTodo = new Todo({\n    text,\n  });\n  return await newTodo.save();\n};\n\n// Update an existing todo\nexport const updateTodo = async (id: string, text: string) => {\n  return await Todo.findByIdAndUpdate(id, { text }, { new: true });\n};\n\n// Delete a todo\nexport const deleteTodo = async (id: string) => {\n  return await Todo.findByIdAndDelete(id);\n};",
#
#   "backend/routes/index.ts": "import express from 'express';\nimport todoRoutes from './todos';\n\nconst router = express.Router();\n\nrouter.use('/todos', todoRoutes);\n\nexport default router;",
#
#   "backend/routes/todos.ts": "import express from 'express';\nimport * as todoController from '../controllers/todoController';\n\nconst router = express.Router();\n\n// Get all todos\nrouter.get('/', todoController.getAllTodos);\n\n// Get todo by ID\nrouter.get('/:id', todoController.getTodoById);\n\n// Add a new todo\nrouter.post('/', todoController.addTodo);\n\n// Update an existing todo\nrouter.put('/:id', todoController.updateTodo);\n\n// Delete a todo\nrouter.delete('/:id', todoController.deleteTodo);\n\nexport default router;",
#
#   "backend/package.json": "{\n  \"name\": \"backend\",\n  \"version\": \"1.0.0\",\n  \"main\": \"app.ts\",\n  \"scripts\": {\n    \"start\": \"ts-node app.ts\",\n    \"dev\": \"nodemon app.ts\",\n    \"build\": \"tsc\"\n  },\n  \"dependencies\": {\n    \"express\": \"^4.17.1\",\n    \"mongoose\": \"^5.10.9\",\n    \"cors\": \"^2.8.5\",\n    \"joi\": \"^17.5.1\"\n  },\n  \"devDependencies\": {\n    \"ts-node\": \"^9.1.1\",\n    \"typescript\": \"^4.3.5\",\n    \"nodemon\": \"^2.0.7\"\n  }\n}"
# }



# Create directories for the project
code_files = {
	"frontend/html/index.html": "<!-- index.html -->\n<!DOCTYPE html>\n<html>\n<head>\n  <title>Tic Tac Toe</title>\n  <link rel=\"stylesheet\" href=\"styles.css\">\n</head>\n<body>\n  <h1>Tic Tac Toe</h1>\n  <div id=\"board\">\n    <!-- Game board will be dynamically generated here -->\n  </div>\n  <script src=\"script.js\"></script>\n</body>\n</html>",

	"frontend/css/styles.css": "/* styles.css */\n#board {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-gap: 10px;\n  width: 300px;\n  margin: 0 auto;\n}\n\n.cell {\n  height: 100px;\n  border: 1px solid black;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  font-size: 24px;\n  cursor: pointer;\n}",

	"frontend/js/script.js": "/* script.js */\n\nconst board = document.getElementById('board');\nconst cells = [];\nlet currentPlayer = null; // 'X' or 'O'\nlet gameBoard = ['', '', '', '', '', '', '', '', '']; // Game state\n\n// Connect to WebSocket server\nconst socket = new WebSocket('ws://localhost:8080');\n\n// Handle incoming WebSocket messages\nsocket.onmessage = function (event) {\n  const message = JSON.parse(event.data);\n\n  if (message.type === 'start') {\n    currentPlayer = message.player;\n    alert(`${currentPlayer}'s turn!`);\n  }\n\n  if (message.type === 'move') {\n    const { index, player } = message;\n    gameBoard[index] = player;\n    updateBoard();\n  }\n\n  if (message.type === 'win') {\n    alert(`${message.player} wins!`);\n    resetBoard();\n  }\n};\n\n// Dynamically create the 3x3 grid of cells\nfor (let i = 0; i < 9; i++) {\n  const cell = document.createElement('div');\n  cell.classList.add('cell');\n  cell.addEventListener('click', () => handleCellClick(i));\n  board.appendChild(cell);\n  cells.push(cell);\n}\n\nfunction handleCellClick(index) {\n  if (gameBoard[index] !== '') return; // Don't allow a move in a filled cell\n  if (currentPlayer === null) return; // Wait for both players to join\n\n  gameBoard[index] = currentPlayer;\n  cells[index].textContent = currentPlayer;\n\n  // Send the move to the server\n  socket.send(JSON.stringify({ type: 'move', index, player: currentPlayer }));\n\n  if (checkWin()) {\n    socket.send(JSON.stringify({ type: 'win', player: currentPlayer }));\n  } else {\n    // Switch player\n    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';\n    alert(`${currentPlayer}'s turn!`);\n  }\n}\n\nfunction checkWin() {\n  const winningCombinations = [\n    [0, 1, 2],\n    [3, 4, 5],\n    [6, 7, 8],\n    [0, 3, 6],\n    [1, 4, 7],\n    [2, 5, 8],\n    [0, 4, 8],\n    [2, 4, 6]\n  ];\n\n  for (const combination of winningCombinations) {\n    const [a, b, c] = combination;\n    if (gameBoard[a] && gameBoard[a] === gameBoard[b] && gameBoard[a] === gameBoard[c]) {\n      return true;\n    }\n  }\n  return false;\n}\n\nfunction updateBoard() {\n  gameBoard.forEach((value, index) => {\n    cells[index].textContent = value;\n  });\n}\n\nfunction resetBoard() {\n  gameBoard = ['', '', '', '', '', '', '', '', ''];\n  updateBoard();\n  currentPlayer = null;\n}",

	"server/server.js": "const WebSocket = require('ws');\nconst wss = new WebSocket.Server({ port: 8080 });\n\nlet clients = []; // Keep track of connected clients\n\n// Broadcast function to send a message to all clients\nfunction broadcast(message) {\n  clients.forEach(client => {\n    if (client.readyState === WebSocket.OPEN) {\n      client.send(JSON.stringify(message));\n    }\n  });\n}\n\nwss.on('connection', (ws) => {\n  // Add new client to the list\n  clients.push(ws);\n\n  // Notify the first player that it's their turn\n  if (clients.length === 2) {\n    clients[0].send(JSON.stringify({ type: 'start', player: 'X' }));\n    clients[1].send(JSON.stringify({ type: 'start', player: 'O' }));\n  }\n\n  // Listen for messages from clients\n  ws.on('message', (message) => {\n    const data = JSON.parse(message);\n\n    // If a player made a move, broadcast it to the other player\n    if (data.type === 'move') {\n      broadcast(data);\n    }\n\n    // If a player wins, notify both players\n    if (data.type === 'win') {\n      broadcast(data);\n    }\n  });\n\n  // Remove client when they disconnect\n  ws.on('close', () => {\n    clients = clients.filter(client => client !== ws);\n  });\n});\n\nconsole.log('WebSocket server is running on ws://localhost:8080');"
}


project_dir = './tic_tac_toe'
frontend_dir = os.path.join(project_dir, 'frontend')
# frontend_src_dir = os.path.join(frontend_dir, 'src')
# frontend_components_dir = os.path.join(frontend_src_dir, 'components')
# backend_dir = os.path.join(project_dir, 'backend')
# backend_models_dir = os.path.join(backend_dir, 'models')
# backend_config_dir = os.path.join(backend_dir, 'config')

directories = [
    frontend_dir
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Write TypeScript frontend and backend files
for filepath, content in code_files.items():
    print(filepath)
    if not os.path.exists(f"./tic_tac_toe/{filepath.rsplit('/',1)[0]}"):
        os.makedirs(f"./tic_tac_toe/{filepath.rsplit('/',1)[0]}")
    with open(f"./tic_tac_toe/{filepath}", 'w') as f:
        f.write(content)
#
# for filepath, content in backend_ts_files.items():
#
#     if not os.path.exists(f"./todolist_ts/{filepath.rsplit('/',1)[0]}"):
#         os.makedirs(f"./todolist_ts/{filepath.rsplit('/',1)[0]}")
#     with open(f"./todolist_ts/{filepath}", 'w') as f:
#         f.write(content)

# Create a ZIP file for the TypeScript version
zip_ts_filepath = "./tic_tac_toe.zip"
with ZipFile(zip_ts_filepath, 'w') as zipf:
    for root, dirs, files in os.walk('./tic_tac_toe'):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), './todolist_ts'))

print(zip_ts_filepath)
