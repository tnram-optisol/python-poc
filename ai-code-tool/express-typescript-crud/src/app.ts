import express from 'express';
import { createConnection } from './database';
import { UserRoutes } from './routes/userRoutes';
import i18n from 'i18n';
import path from 'path';

const app = express();
const port = process.env.PORT || 5000;

// Initialize i18n
i18n.configure({
  locales: ['en'],
  directory: path.join(__dirname, '/constants'),
  defaultLocale: 'en',
});

// Middleware setup
app.use(i18n.init);
app.use(express.json());

// Database connection
createConnection();

// Register routes
UserRoutes.registerRoutes(app);

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
