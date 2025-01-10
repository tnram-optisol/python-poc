import { Request, Response } from 'express';
import * as todoService from '../services/todoService';
import { todoValidationSchema } from '../validators/todoValidator';
import Joi from 'joi';

// Get all todos
export const getAllTodos = async (req: Request, res: Response) => {
  try {
    const todos = await todoService.getAllTodos();
    res.json(todos);
  } catch (err) {
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

// Get todo by ID
export const getTodoById = async (req: Request, res: Response) => {
  const { id } = req.params;
  try {
    const todo = await todoService.getTodoById(id);
    if (!todo) {
      return res.status(404).json({ message: 'Todo not found' });
    }
    res.json(todo);
  } catch (err) {
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

// Add a new todo
export const addTodo = async (req: Request, res: Response) => {
  const { text } = req.body;

  // Validate the request body
  const { error } = todoValidationSchema.validate({ text });
  if (error) {
    return res.status(400).json({
      message: 'Validation error',
      details: error.details,
    });
  }

  try {
    const newTodo = await todoService.addTodo(text);
    res.json(newTodo);
  } catch (err) {
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

// Update an existing todo
export const updateTodo = async (req: Request, res: Response) => {
  const { id } = req.params;
  const { text } = req.body;

  // Validate the request body
  const { error } = todoValidationSchema.validate({ text });
  if (error) {
    return res.status(400).json({
      message: 'Validation error',
      details: error.details,
    });
  }

  try {
    const updatedTodo = await todoService.updateTodo(id, text);
    if (!updatedTodo) {
      return res.status(404).json({ message: 'Todo not found' });
    }
    res.json(updatedTodo);
  } catch (err) {
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

// Delete a todo
export const deleteTodo = async (req: Request, res: Response) => {
  const { id } = req.params;
  try {
    const deletedTodo = await todoService.deleteTodo(id);
    if (!deletedTodo) {
      return res.status(404).json({ message: 'Todo not found' });
    }
    res.json({ message: 'Todo deleted successfully' });
  } catch (err) {
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};