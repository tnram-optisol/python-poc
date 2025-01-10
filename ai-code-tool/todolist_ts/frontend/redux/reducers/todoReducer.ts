import { SET_TODOS, ADD_TODO, DELETE_TODO } from '../actions/todoActions';

interface Todo {
  _id: string;
  text: string;
}

interface TodoState {
  todos: Todo[];
}

const initialState: TodoState = {
  todos: [],
};

const todoReducer = (state = initialState, action: any): TodoState => {
  switch (action.type) {
    case SET_TODOS:
      return { ...state, todos: action.payload };
    case ADD_TODO:
      return { ...state, todos: [...state.todos, action.payload] };
    case DELETE_TODO:
      return { ...state, todos: state.todos.filter((todo) => todo._id !== action.payload) };
    default:
      return state;
  }
};

export default todoReducer;