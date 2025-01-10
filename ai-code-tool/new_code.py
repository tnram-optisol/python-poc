import os
import zipfile

# Define the project directory and files to create
project_dir = 'express-typescript-crud/src'
file_structure = {
    'app.ts': '''import express from 'express';
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
''',
    'database.ts': '''import mongoose from 'mongoose';

export const createConnection = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/express_ts_crud');
    console.log('MongoDB connected');
  } catch (err) {
    console.error('Database connection failed:', err);
    process.exit(1);
  }
};
''',
    'constants/en.json': '''{
  "USER_CREATED": "User created successfully",
  "USER_NOT_FOUND": "User not found",
  "USER_DELETED": "User deleted successfully",
  "USER_UPDATED": "User updated successfully",
  "USER_NAME_REQUIRED": "User name is required",
  "USER_EMAIL_REQUIRED": "User email is required"
}
''',
    'models/userModel.ts': '''import mongoose, { Schema, Document } from 'mongoose';

export interface IUser extends Document {
  name: string;
  email: string;
}

const userSchema: Schema = new Schema(
  {
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true }
  },
  { timestamps: true }
);

export const User = mongoose.model<IUser>('User', userSchema);
''',
    'controllers/userController.ts': '''import { Request, Response } from 'express';
import { UserService } from '../services/userService';
import i18n from 'i18n';
import { Controller, Get, Post, Put, Delete, Body, Param } from '../decorators';

@Controller('/users')
export class UserController {
  @Post('/')
  static async createUser(@Body() body: { name: string, email: string }, res: Response) {
    try {
      const user = await UserService.createUser(body);
      return res.status(201).json({ message: i18n.__('USER_CREATED'), user });
    } catch (err) {
      return res.status(500).json({ message: err.message });
    }
  }

  @Get('/:id')
  static async getUser(@Param('id') id: string, res: Response) {
    try {
      const user = await UserService.getUser(id);
      if (!user) {
        return res.status(404).json({ message: i18n.__('USER_NOT_FOUND') });
      }
      return res.status(200).json(user);
    } catch (err) {
      return res.status(500).json({ message: err.message });
    }
  }

  @Put('/:id')
  static async updateUser(@Param('id') id: string, @Body() body: { name: string, email: string }, res: Response) {
    try {
      const user = await UserService.updateUser(id, body);
      if (!user) {
        return res.status(404).json({ message: i18n.__('USER_NOT_FOUND') });
      }
      return res.status(200).json({ message: i18n.__('USER_UPDATED'), user });
    } catch (err) {
      return res.status(500).json({ message: err.message });
    }
  }

  @Delete('/:id')
  static async deleteUser(@Param('id') id: string, res: Response) {
    try {
      const user = await UserService.deleteUser(id);
      if (!user) {
        return res.status(404).json({ message: i18n.__('USER_NOT_FOUND') });
      }
      return res.status(200).json({ message: i18n.__('USER_DELETED') });
    } catch (err) {
      return res.status(500).json({ message: err.message });
    }
  }
}
''',
    'routes/userRoutes.ts': '''import { registerRoutes } from '../decorators';
import { UserController } from '../controllers/userController';

export class UserRoutes {
  static registerRoutes(app: any) {
    registerRoutes(app, UserController);
  }
}
''',
    'services/userService.ts': '''import { User, IUser } from '../models/userModel';

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
''',
    'middlewares/errorHandler.ts': '''import { Request, Response, NextFunction } from 'express';

export const errorHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Internal server error' });
};
''',
    'decorators/index.ts': '''import 'reflect-metadata';
import { Request, Response, NextFunction } from 'express';

// Route decorators
export function Controller(route: string) {
  return function (target: Function) {
    target.prototype.baseRoute = route;
  };
}

export function Get(path: string) {
  return function (target: any, key: string, descriptor: PropertyDescriptor) {
    Reflect.defineMetadata('route', { method: 'get', path }, target, key);
  };
}

export function Post(path: string) {
  return function (target: any, key: string, descriptor: PropertyDescriptor) {
    Reflect.defineMetadata('route', { method: 'post', path }, target, key);
  };
}

export function Put(path: string) {
  return function (target: any, key: string, descriptor: PropertyDescriptor) {
    Reflect.defineMetadata('route', { method: 'put', path }, target, key);
  };
}

export function Delete(path: string) {
  return function (target: any, key: string, descriptor: PropertyDescriptor) {
    Reflect.defineMetadata('route', { method: 'delete', path }, target, key);
  };
}

// Parameter decorators
export function Body() {
  return function (target: any, key: string, index: number) {
    const existingBodyParams = Reflect.getMetadata('bodyParams', target, key) || [];
    existingBodyParams.push(index);
    Reflect.defineMetadata('bodyParams', existingBodyParams, target, key);
  };
}

export function Param(paramName: string) {
  return function (target: any, key: string, index: number) {
    const existingParams = Reflect.getMetadata('paramParams', target, key) || {};
    existingParams[paramName] = index;
    Reflect.defineMetadata('paramParams', existingParams, target, key);
  };
}

export function Query(paramName: string) {
  return function (target: any, key: string, index: number) {
    const existingQueryParams = Reflect.getMetadata('queryParams', target, key) || {};
    existingQueryParams[paramName] = index;
    Reflect.defineMetadata('queryParams', existingQueryParams, target, key);
  };
}

// Route registration handler
export function registerRoutes(app: any, controller: any) {
  const controllerInstance = new controller();
  const baseRoute = controllerInstance.baseRoute;

  const methods = Object.getOwnPropertyNames(controller.prototype);
  methods.forEach((method) => {
    const routeMetadata = Reflect.getMetadata('route', controller.prototype, method);
    if (routeMetadata) {
      const { method: httpMethod, path } = routeMetadata;
      const fullPath = baseRoute + path;

      // Get parameters (Body, Param, Query)
      const bodyParams = Reflect.getMetadata('bodyParams', controller.prototype, method) || [];
      const paramParams = Reflect.getMetadata('paramParams', controller.prototype, method) || {};
      const queryParams = Reflect.getMetadata('queryParams', controller.prototype, method) || {};

      // Register route
      app[httpMethod](fullPath, (req: Request, res: Response, next: NextFunction) => {
        const args = [];

        // Extract body
        bodyParams.forEach((index: number) => {
          args[index] = req.body;
        });

        // Extract path params
        Object.keys(paramParams).forEach((param) => {
          args[paramParams[param]] = req.params[param];
        });

        // Extract query params
        Object.keys(queryParams).forEach((query) => {
          args[queryParams[query]] = req.query[query];
        });

        // Call the method with extracted parameters
        controllerInstance[method](...args, res, req);
      });
    }
  });
}
''',
    'package.json':'''
    {
  "name": "express-ts-mongo-crud",
  "version": "1.0.0",
  "main": "src/app.ts",
  "scripts": {
    "dev": "ts-node-dev --respawn --transpileOnly src/app.ts",
    "build": "tsc",
    "start": "node dist/app.js"
  },
  "dependencies": {
    "express": "^4.18.1",
    "mongoose": "^6.6.5",
    "i18n": "^0.13.2",
    "reflect-metadata": "^0.1.13",
    "class-validator": "^0.14.0",
    "class-transformer": "^0.5.1"
  },
  "devDependencies": {
    "typescript": "^4.5.4",
    "ts-node-dev": "^1.1.8",
    "@types/express": "^4.17.13",
    "@types/mongoose": "^5.10.5"
  }
}

    ''',
    "tsconfig.json":'''
    {
  "compilerOptions": {
    "target": "ES6",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "strict": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}

    '''
}

# Function to create the project structure
def create_project():
    for file_path, content in file_structure.items():
        full_path = os.path.join(project_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

# Function to zip the project
def zip_project(zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), project_dir))
    zipf.close()

# Create the project
create_project()

# Zip the project
zip_project('project.zip')

print("Project zipped successfully!")
