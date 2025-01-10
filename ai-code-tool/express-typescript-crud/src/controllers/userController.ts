import { Request, Response } from 'express';
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
