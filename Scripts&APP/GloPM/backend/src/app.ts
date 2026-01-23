import { Hono } from 'hono';
import { connectToMongoDB } from './utils/mongoDB';
import { authRoutes } from './routes/authRoutes';
import { packageRoutes } from './routes/packageRoutes';
import { PORT } from './config';
import { serve } from '@hono/node-server';

const app = new Hono();

// 根路由
app.get('/', (c) => c.text('GloPM Backend are running!'));

// 异步启动服务器
(async () => {
  try {
    const db = await connectToMongoDB();

    // 挂载认证路由组到 /api/auth
    const authRouter = authRoutes(db);
    app.route('/api/auth', authRouter);

    // 挂载包管理路由组到 /api/packages
    const packageRouter = packageRoutes(db);
    app.route('/api/packages', packageRouter);

    // 启动服务器
    const port = PORT || 9009;
    serve({
      fetch: app.fetch,
      port: parseInt(port as string)
    });
  } catch (error) {
    console.error('服务器启动失败:', error);
    process.exit(1);
  }
})();
