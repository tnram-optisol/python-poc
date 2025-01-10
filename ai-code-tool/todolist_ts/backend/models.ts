import mongoose, { Schema, Document } from 'mongoose';

interface ITodo extends Document {
  text: string;
}

const TodoSchema: Schema = new Schema({
  text: {
    type: String,
    required: true,
  },
});

const Todo = mongoose.model<ITodo>('Todo', TodoSchema);

export default Todo;