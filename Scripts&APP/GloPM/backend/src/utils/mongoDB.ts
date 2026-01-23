// src/utils/mongoDB.ts
// 建立 MongoDB 连接后再启动服务器
import { MongoClient, Db } from 'mongodb';
import { MONGO_CONNECTION_STRING, DB_NAME } from '../config';

// 单例模式保存 MongoDB 连接
let client: MongoClient | null = null;
let database: Db | null = null;

/**
 * 连接到 MongoDB 数据库
 * @returns Promise<Db> 数据库实例
 */
export async function connectToMongoDB(): Promise<Db> {
  if (database) {
    return database;
  }

  if (!MONGO_CONNECTION_STRING) {
    while (true) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      console.log('MONGO_CONNECTION_STRING 未配置');
    }
  }

  try {
    client = await MongoClient.connect(MONGO_CONNECTION_STRING);
    database = client.db(DB_NAME);
    console.log('MongoDB 连接成功');
    return database;
  } catch (error) {
    console.error('MongoDB 连接失败:', error);
    throw error;
  }
}

/**
 * 获取数据库实例
 * @returns Db | null 数据库实例，如果未连接则返回 null
 */
export function getDatabase(): Db | null {
  return database;
}

/**
 * 关闭 MongoDB 连接
 */
export async function closeMongoDB(): Promise<void> {
  if (client) {
    await client.close();
    client = null;
    database = null;
    console.log('MongoDB 连接已关闭');
  }
}

// 处理进程退出时关闭数据库连接
process.on('SIGINT', async () => {
  await closeMongoDB();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await closeMongoDB();
  process.exit(0);
});
