import mongoose, { Schema, Document } from 'mongoose';

export interface IUser extends Document {
  name: string;
  email: string;
  phone: string;
  isActive: boolean;
  createdAt?: Date;
  updatedAt?: Date;
  address?: string;
  role: string;
}

const userSchema: Schema = new Schema(
  {
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    phone: { type: String, required: true },
    address: { type: String },
    isActive: { type: Boolean, default: true },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date }
  },
  { timestamps: true }
);

export const User = mongoose.model<IUser>('User', userSchema);
