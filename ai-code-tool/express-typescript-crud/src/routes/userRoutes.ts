import { registerRoutes } from '../decorators';
import { UserController } from '../controllers/userController';

export class UserRoutes {
  static registerRoutes(app: any) {
    registerRoutes(app, UserController);
  }
}
