// src/controllers/packageController.ts
import { Context } from 'hono';
import { Db, ObjectId, GridFSBucket } from 'mongodb';
import { saveFileToGridFS } from '../utils/gridFS';

export class PackageController {
  private db: Db;
  private gridFSBucket: GridFSBucket;

  constructor(db: Db) {
    this.db = db;
    this.gridFSBucket = new GridFSBucket(db, { bucketName: 'fs' });
  }

  /**
   * 发布包
   * PUT /api/packages/publish
   * 表单字段：packageName, version, description, file（文件对象）
   */
  async publish(c: Context) {
    try {
      // 从请求头获取用户 ID（假设经过中间件认证后设置到环境变量中）
      const userIdHeader = c.req.header('x-user-id');
      if (!userIdHeader) {
        return c.json({ error: '未认证' }, 401);
      }
      const userId = new ObjectId(userIdHeader);

      // 解析 multipart 表单数据（需保证请求 Content-Type 为 multipart/form-data）
      const formData = await c.req.formData();
      const packageName = formData.get('packageName');
      const version = formData.get('version');
      const description = formData.get('description');
      const fileField = formData.get('file');

      if (!packageName || !version || !description) {
        return c.json({ error: '缺少必要字段' }, 400);
      }

      if (!fileField || !(fileField instanceof File)) {
        return c.json({ error: '文件未上传或格式错误' }, 400);
      }

      // 将上传的 File 对象转换为 Buffer
      const fileBuffer = Buffer.from(await fileField.arrayBuffer());
      const fileName = fileField.name;

      // 查找包是否存在
      let pkg = await this.db.collection('packages').findOne({ name: packageName });
      if (pkg) {
        // 判断当前用户是否为拥有者
        if (!pkg.owner.equals(userId)) {
          return c.json({ error: '无权限发布此包' }, 403);
        }
        await this.db.collection('packages').updateOne(
          { _id: pkg._id },
          {
            $set: {
              description,
              owner: userId,
              updatedAt: new Date(),
            }
          }
        )
      } else {
        // 插入新包记录
        const result = await this.db.collection('packages').insertOne({
          name: packageName,
          description,
          owner: userId,
          createdAt: new Date(),
          updatedAt: new Date(),
        });
        pkg = { _id: result.insertedId };
      }

      // 检查版本是否已存在
      const existingVersion = await this.db.collection('versions').findOne({
        package: pkg._id,
        version
      });
      if (existingVersion) {
        return c.json({ error: '版本已存在' }, 400);
      }

      // 上传文件到 GridFS
      const fileId = await saveFileToGridFS(this.gridFSBucket, fileBuffer, {
        filename: fileName,
        metadata: {
          packageName,
          version
        }
      });

      // 插入版本记录
      const versionResult = await this.db.collection('versions').insertOne({
        package: pkg._id,
        version,
        description,
        fileSize: fileBuffer.length,
        filePath: fileId.toHexString(),
        filename: fileName,
        publishedBy: userId,
        publishedAt: new Date(),
        downloads: 0
      });

      return c.json({ message: '包发布成功', versionId: versionResult.insertedId });
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /** 删除版本
   * DELETE /api/packages/:packageName/versions/:version
   */
  async deleteVersion(c: Context) {
    try {
      const userIdHeader = c.req.header('x-user-id');
      if (!userIdHeader) {
        return c.json({ error: '未认证' }, 401);
      }
      const userId = new ObjectId(userIdHeader);

      const packageName = c.req.param('packageName');
      const version = c.req.param('version');

      const pkg = await this.db.collection('packages').findOne({ name: packageName });
      if (!pkg) {
        return c.json({ error: '包不存在' }, 404);
      }
      if (!pkg.owner.equals(userId)) {
        return c.json({ error: '无权限删除此包' }, 403);
      }
      await this.db.collection('versions').deleteOne({ package: pkg._id, version });
      return c.json({ message: '版本删除成功' });
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /**
   * 删除包
   * DELETE /api/packages/:packageName
   */
  async deletePackage(c: Context) {
    try {
      const userIdHeader = c.req.header('x-user-id');
      if (!userIdHeader) {
        return c.json({ error: '未认证' }, 401);
      }
      const userId = new ObjectId(userIdHeader);

      const packageName = c.req.param('packageName');
      const pkg = await this.db.collection('packages').findOne({ name: packageName });
      if (!pkg) {
        return c.json({ error: '包不存在' }, 404);
      }
      if (!pkg.owner.equals(userId)) {
        return c.json({ error: '无权限删除此包' }, 403);
      }
      await this.db.collection('packages').deleteOne({ _id: pkg._id });
      await this.db.collection('versions').deleteMany({ package: pkg._id });
      return c.json({ message: '包删除成功' });
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /**
   * 下载包
   * GET /api/packages/:packageName/download/:version
   */
  async download(c: Context) {
    try {
      const packageName = c.req.param('packageName');
      const version = c.req.param('version');
      const pkg = await this.db.collection('packages').findOne({ name: packageName });
      if (!pkg) {
        return c.json({ error: '包不存在' }, 404);
      }
      const versionInfo = await this.db.collection('versions').findOne({
        package: pkg._id,
        version: version
      });
      if (!versionInfo) {
        return c.json({ error: '版本不存在' }, 404);
      }

      // 从 GridFS 中获取文件
      const fileId = new ObjectId(versionInfo.filePath as string);
      const downloadStream = this.gridFSBucket.openDownloadStream(fileId);
      
      // 增加downloads
      await this.db.collection('versions').updateOne({ _id: versionInfo._id }, { $inc: { downloads: 1 } });

      // 将流转换为 Buffer
      const chunks: Buffer[] = [];
      for await (const chunk of downloadStream) {
        chunks.push(Buffer.from(chunk));
      }
      const fileBuffer = Buffer.concat(chunks);
      
      c.header('Content-Type', 'application/octet-stream');
      c.header('Content-Disposition', `attachment; filename="${versionInfo.filename}"`);
      
      return c.body(fileBuffer);
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /**
   * 搜索包
   * GET /api/packages/search?query=xxx
   */
  async searchPackages(c: Context) {
    try {
      const query = c.req.query('query') || '';
      const packages = await this.db
        .collection('packages')
        .find({ name: { $regex: query, $options: 'i' } })
        .toArray();
      return c.json(packages);
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /**
   * 获取最新版本
   * GET /api/packages/:packageName/ver
   */
  async getLatestVersion(c: Context) {
    try {
      const packageName = c.req.param('packageName');
      const pkg = await this.db.collection('packages').findOne({ name: packageName });
      if (!pkg) {
        return c.json({ error: '包不存在' }, 404);
      }
      const latestVersion = await this.db
        .collection('versions')
        .find({ package: pkg._id })
        .sort({ publishedAt: -1 })
        .limit(1)
        .toArray();
      if (latestVersion.length === 0) {
        return c.json({ message: '暂无版本' });
      } else {
        return c.json(latestVersion[0]);
      }
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }

  /**
   * 获取包版本列表
   * GET /api/packages/:packageName/versions
   */
  async getPackageVersions(c: Context) {
    try {
      const packageName = c.req.param('packageName');
      const pkg = await this.db.collection('packages').findOne({ name: packageName });
      if (!pkg) {
        return c.json({ error: '包不存在' }, 404);
      }
      const versions = await this.db.collection('versions').find({ package: pkg._id }).toArray();
      return c.json(versions);
    } catch (error: any) {
      return c.json({ error: error.message }, 500);
    }
  }
  
}
