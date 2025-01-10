import mongoose from 'mongoose';

export const createConnection = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/express_ts_crud');
    console.log('MongoDB connected');
  } catch (err) {
    console.error('Database connection failed:', err);
    process.exit(1);
  }
};
