import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTodos, createTodo, removeTodo } from '../redux/actions/todoActions';
import TodoItem from './TodoItem';

interface Todo {
  _id: string;
  text: string;
}

const TodoList: React.FC = () => {
  const [newTodo, setNewTodo] = useState<string>('');
  const dispatch = useDispatch();
  const todos = useSelector((state: any) => state.todos);

  useEffect(() => {
    dispatch(fetchTodos());
  }, [dispatch]);

  const addTodo = () => {
    if (newTodo.trim()) {
      dispatch(createTodo(newTodo));
      setNewTodo('');
    }
  };

  const deleteTodo = (id: string) => {
    dispatch(removeTodo(id));
  };

  return (
    <div className="todo-container">
      <div className="todo-input">
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Enter a new todo"
        />
        <button onClick={addTodo}>Add Todo</button>
      </div>

      <ul className="todo-list">
        {todos.map((todo: Todo) => (
          <TodoItem key={todo._id} todo={todo} onDelete={deleteTodo} />
        ))}
      </ul>
    </div>
  );
};

export default TodoList;