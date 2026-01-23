// src/routes/authRoutes.ts
import { Hono } from 'hono';
import { AuthController } from '../controllers/authController';
import { authenticate } from '../middlewares/auth';
import { Db } from 'mongodb';

/**
 * 用户认证相关路由
 */
export function authRoutes(db: Db): Hono {
  const app = new Hono();
  const authController = new AuthController(db);

  // 用户注册
  app.post('/register', async (c) => {
    return await authController.register(c);
  });

  // 用户登录
  app.post('/login', async (c) => {
    return await authController.login(c);
  });

  // 删除用户
  app.delete('/', authenticate(db), async (c) => {
    return await authController.removeAccount(c);
  });

  return app;
}