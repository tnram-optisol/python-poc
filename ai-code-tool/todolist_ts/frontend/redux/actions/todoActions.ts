import { Dispatch } from 'redux';

interface Todo {
  _id: string;
  text: string;
}

// Action Types
const SET_TODOS = 'SET_TODOS';
const ADD_TODO = 'ADD_TODO';
const DELETE_TODO = 'DELETE_TODO';

// Action Creators
const setTodos = (todos: Todo[]) => ({
  type: SET_TODOS,
  payload: todos,
});

const addTodo = (todo: Todo) => ({
  type: ADD_TODO,
  payload: todo,
});

const deleteTodo = (id: string) => ({
  type: DELETE_TODO,
  payload: id,
});

// Thunk actions
export const fetchTodos = () => {
  return async (dispatch: Dispatch) => {
    const res = await fetch('/api/todos');
    const data = await res.json();
    dispatch(setTodos(data));
  };
};

export const createTodo = (text: string) => {
  return async (dispatch: Dispatch) => {
    const res = await fetch('/api/todos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    const newTodo = await res.json();
    dispatch(addTodo(newTodo));
  };
};

export const removeTodo = (id: string) => {
  return async (dispatch: Dispatch) => {
    await fetch(`/api/todos/${id}`, { method: 'DELETE' });
    dispatch(deleteTodo(id));
  };
};