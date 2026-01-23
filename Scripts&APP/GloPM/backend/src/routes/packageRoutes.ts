// src/routes/packageRoutes.ts
import { Hono } from 'hono';
import { PackageController } from '../controllers/packageController';
import { authenticate } from '../middlewares/auth';
import { Db } from 'mongodb';

export function packageRoutes(db: Db): Hono {
  const app = new Hono();
  const packageController = new PackageController(db);

  // 发布包 (需要认证)
  app.put('/publish', authenticate(db), async (c) => {
    return await packageController.publish(c);
  });

  // 删除包 (需要认证)
  app.delete('/:packageName', authenticate(db), async (c) => {
    return await packageController.deletePackage(c);
  });

  // 下载包 (无需认证)
  app.get('/:packageName/download/:version', async (c) => {
    return await packageController.download(c);
  });

  // 搜索包
  app.get('/search', async (c) => {
    return await packageController.searchPackages(c);
  });

  // 获取最新版本号
  app.get('/:packageName/latestVersion', async (c) => {
    return await packageController.getLatestVersion(c);
  });

  // 获取包版本列表
  app.get('/:packageName/versions', async (c) => {
    return await packageController.getPackageVersions(c);
  });

  return app;
}