import express from 'express';
import todoRoutes from './todos';

const router = express.Router();

router.use('/todos', todoRoutes);

export default router;