import React from 'react';

interface Todo {
  text: string;
  _id: string;
}

interface TodoItemProps {
  todo: Todo;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onDelete }) => {
  return (
    <li className="todo-item">
      {todo.text}
      <button onClick={() => onDelete(todo._id)}>Delete</button>
    </li>
  );
};

export default TodoItem;