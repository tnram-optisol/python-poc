import mongoose, { Document, Schema } from 'mongoose';

interface ITodo extends Document {
  text: string;
}

const TodoSchema: Schema = new Schema({
  text: {
    type: String,
    required: true
  }
});

export default mongoose.model<ITodo>('Todo', TodoSchema);