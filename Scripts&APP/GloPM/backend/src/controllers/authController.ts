// src/controllers/authController.ts
import { Context } from 'hono';
import { Db, ObjectId } from 'mongodb';
import argon2 from 'argon2';
import crypto from 'node:crypto';
/**
 * 生成统一 API Key 的示例方法
 */
export function generateApiKey(): string {
    return crypto.randomBytes(32).toString('hex');
}

export class AuthController {
  private db: Db;

  constructor(db: Db) {
    this.db = db;
  }

  /**
   * 用户注册
   * POST /api/auth/register
   * body: { username, password }
   */
  async register(c: Context) {
    try {
      const data = await c.req.json();
      const { username, password } = data;
      if (!username || !password) {
        return c.json({ error: '缺少用户名或密码' }, 400);
      }

      const hashedPassword = await argon2.hash(password);
      const api_key = generateApiKey();

      const result = await this.db.collection('users').insertOne({
        username,
        password: hashedPassword,
        api_key
      });

      return c.json({ user_id: result.insertedId, api_key: api_key }, 201);
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /**
   * 用户登录（示例实现）
   * POST /api/auth/login
   * body: { username, password }
   */
  async login(c: Context) {
    try {
      const data = await c.req.json();
      const { username, password } = data;
      if (!username || !password) {
        return c.json({ error: '缺少用户名或密码' }, 400);
      }
      const user = await this.db.collection('users').findOne({ username });
      if (!user) {
        return c.json({ error: '用户不存在' }, 404);
      }
      if (!(await argon2.verify(user.password, password))) {
        return c.json({ error: '密码错误' }, 401);
      }
      return c.json({ user_id: user._id, api_key: user.api_key });
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /**
   * 删除账号（示例实现）
   * DELETE /api/auth/
   * header: x-api-key, x-user-id
   */
  async removeAccount(c: Context) {
    try {
      const userId = c.env.userId;
      if (!userId) {
        return c.json({ error: '未认证' }, 401);
      }
      await this.db.collection('users').deleteOne({ _id: new ObjectId(userId) });
      return c.json({ message: '用户删除成功' });
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }
}
