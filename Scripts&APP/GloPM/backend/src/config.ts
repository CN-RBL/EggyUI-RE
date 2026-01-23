// src/config.ts
import dotenv from 'dotenv';
import path from 'path';

// 加载 .env 文件
dotenv.config({ path: path.resolve(__dirname, '.env') });

/**
 * MongoDB 数据库连接字符串
 * 例如：'mongodb://localhost:27017/npmdb'
 */
export const MONGO_CONNECTION_STRING = process.env.MONGO_CONNECTION_STRING || dotenv.config().parsed?.MONGO_CONNECTION_STRING;

/**
 * 使用的数据库名称
 */
export const DB_NAME = process.env.DB_NAME || dotenv.config().parsed?.DB_NAME;

/**
 * 服务监听的端口
 */
export const PORT = process.env.PORT || dotenv.config().parsed?.PORT;

// 检查必要的环境变量
if (!MONGO_CONNECTION_STRING) {
  console.warn('警告: MONGO_CONNECTION_STRING 未配置，使用默认值');
}
