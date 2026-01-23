// src/utils/gridFS.ts
import { GridFSBucket, ObjectId, GridFSBucketWriteStreamOptions } from 'mongodb';
import { Readable } from 'node:stream';

/**
 * 上传文件 Buffer 到 GridFS 并返回文件的 ObjectID
 * @param bucket GridFSBucket 实例
 * @param buffer 文件的二进制数据
 * @param options 包含 filename 与 metadata 的写入选项
 */
export function saveFileToGridFS(
  bucket: GridFSBucket,
  buffer: Buffer,
  options: GridFSBucketWriteStreamOptions & { filename: string }
): Promise<ObjectId> {
  return new Promise((resolve, reject) => {
    const readable = new Readable();
    // 将 Buffer 数据推入可读流
    readable.push(buffer);
    readable.push(null);

    const uploadStream = bucket.openUploadStream(options.filename, {
      metadata: options.metadata
    });
    readable.pipe(uploadStream);

    uploadStream.on('error', (err) => {
      reject(err);
    });

    uploadStream.on('finish', () => {
      resolve(uploadStream.id as ObjectId);
    });
  });
}

/**
 * 根据文件 ID 获取从 GridFS 的流
 * @param bucket GridFSBucket 实例
 * @param fileId 字符串形式的 ObjectID
 */
export function getFileStreamFromGridFS(bucket: GridFSBucket, fileId: string) {
  return bucket.openDownloadStream(new ObjectId(fileId));
}