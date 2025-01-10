import Todo from '../models';

// Get all todos
export const getAllTodos = async () => {
  return await Todo.find();
};

// Get a single todo by ID
export const getTodoById = async (id: string) => {
  return await Todo.findById(id);
};

// Add a new todo
export const addTodo = async (text: string) => {
  const newTodo = new Todo({
    text,
  });
  return await newTodo.save();
};

// Update an existing todo
export const updateTodo = async (id: string, text: string) => {
  return await Todo.findByIdAndUpdate(id, { text }, { new: true });
};

// Delete a todo
export const deleteTodo = async (id: string) => {
  return await Todo.findByIdAndDelete(id);
};