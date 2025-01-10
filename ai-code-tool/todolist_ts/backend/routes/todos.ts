import express from 'express';
import * as todoController from '../controllers/todoController';

const router = express.Router();

// Get all todos
router.get('/', todoController.getAllTodos);

// Get todo by ID
router.get('/:id', todoController.getTodoById);

// Add a new todo
router.post('/', todoController.addTodo);

// Update an existing todo
router.put('/:id', todoController.updateTodo);

// Delete a todo
router.delete('/:id', todoController.deleteTodo);

export default router;