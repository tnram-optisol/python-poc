import 'reflect-metadata';
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
