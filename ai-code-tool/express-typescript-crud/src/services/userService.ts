import { User, IUser } from '../models/userModel';

export class UserService {
  static async createUser(userData: { name: string; email: string }): Promise<IUser> {
    const user = new User(userData);
    return await user.save();
  }

  static async getUser(id: string): Promise<IUser | null> {
    return await User.findById(id);
  }

  static async updateUser(id: string, userData: { name: string; email: string }): Promise<IUser | null> {
    return await User.findByIdAndUpdate(id, userData, { new: true });
  }

  static async deleteUser(id: string): Promise<IUser | null> {
    return await User.findByIdAndDelete(id);
  }
}
