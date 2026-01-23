// src/middlewares/auth.ts
import { MiddlewareHandler } from 'hono';
import { Db, ObjectId } from 'mongodb';

export function authenticate(db: Db): MiddlewareHandler {
  return async (c, next) => {
    const apiKey = c.req.header('x-api-key');
    const userId = c.req.header('x-user-id');

    if (!apiKey) {
      return c.json({ error: '缺少 API Key' }, 401);
    }
    if (!userId) {
      return c.json({ error: '缺少 User ID' }, 401);
    }

    const user = await db.collection('users').findOne({ _id: new ObjectId(userId) });
    if (!user) {
      return c.json({ error: '无效的 User' }, 401);
    }
    if (user.api_key !== apiKey) {
      return c.json({ error: '错误的 API Key' }, 401);
    }

    // 将 userId 保存到环境中，方便后续使用
    c.env.userId = userId;
    return next();
  };
}
