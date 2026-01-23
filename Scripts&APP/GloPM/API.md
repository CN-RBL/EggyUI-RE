# GloPM API 接口文档

## 基本信息

- **基础 URL**: `https://glopm-backend.zeabur.app/api`
- **API 版本**: v1.0.0
- **认证方式**: 用户 ID 和 API Key 通过请求头传递

## 认证

所有需要认证的接口都需要在请求头中包含以下信息：

```
x-user-id: <用户ID>
x-api-key: <API密钥>
```

## 接口列表

### 用户认证

#### 注册

- **URL**: `/auth/register`
- **方法**: `POST`
- **描述**: 注册新用户
- **请求体**:
  ```json
  {
    "username": "用户名",
    "password": "密码"
  }
  ```
- **响应**:
  ```json
  {
    "user_id": "用户ID",
    "api_key": "API密钥"
  }
  ```

#### 登录

- **URL**: `/auth/login`
- **方法**: `POST`
- **描述**: 用户登录
- **请求体**:
  ```json
  {
    "username": "用户名",
    "password": "密码"
  }
  ```
- **响应**:
  ```json
  {
    "user_id": "用户ID",
    "api_key": "API密钥"
  }
  ```

#### 删除账户

- **URL**: `/auth/`
- **方法**: `DELETE`
- **描述**: 删除当前用户账户
- **需要认证**: 是
- **响应**:
  ```json
  {
    "message": "账户已成功删除"
  }
  ```

### 包管理

#### 发布包

- **URL**: `/packages/publish`
- **方法**: `PUT`
- **描述**: 发布新包或更新现有包
- **需要认证**: 是
- **请求体**:
  - 使用 `multipart/form-data` 格式
  - 字段:
    - `packageName`: 包名
    - `version`: 版本号
    - `description`: 包描述
    - `file`: 包文件
- **响应**:
  ```json
  {
    "id": "包ID",
    "name": "包名",
    "version": "版本号",
    "description": "包描述",
    "fileSize": 文件大小(字节),
    "publishedAt": "发布时间(ISO格式)"
  }
  ```

#### 下载包

- **URL**: `/packages/{packageName}/download/{version}`
- **方法**: `GET`
- **描述**: 下载指定包和版本
- **需要认证**: 否
- **参数**:
  - `packageName`: 包名
  - `version`: 版本号，可使用 `latest` 获取最新版本
- **响应**: 文件流

#### 搜索包

- **URL**: `/packages/search`
- **方法**: `GET`
- **描述**: 搜索包
- **需要认证**: 否
- **参数**:
  - `query`: 搜索关键词
- **响应**:
  ```json
  [
    {
      "id": "包ID",
      "name": "包名",
      "description": "包描述",
      "latestVersion": "最新版本",
      "updatedAt": "更新时间(ISO格式)"
    },
    ...
  ]
  ```

#### 获取包最新版本

- **URL**: `/packages/{packageName}/latestVersion`
- **方法**: `GET`
- **描述**: 获取包的最新版本信息
- **需要认证**: 否
- **参数**:
  - `packageName`: 包名
- **响应**:
  ```json
  {
    "version": "版本号",
    "description": "版本描述",
    "fileSize": 文件大小(字节),
    "publishedAt": "发布时间(ISO格式)",
    "downloads": 下载次数
  }
  ```

#### 获取包所有版本

- **URL**: `/packages/{packageName}/versions`
- **方法**: `GET`
- **描述**: 获取包的所有版本信息
- **需要认证**: 否
- **参数**:
  - `packageName`: 包名
- **响应**:
  ```json
  [
    {
      "version": "版本号",
      "description": "版本描述",
      "fileSize": 文件大小(字节),
      "publishedAt": "发布时间(ISO格式)",
      "downloads": 下载次数
    },
    ...
  ]
  ```

#### 删除包

- **URL**: `/packages/{packageName}`
- **方法**: `DELETE`
- **描述**: 删除指定包（包括所有版本）
- **需要认证**: 是
- **参数**:
  - `packageName`: 包名
- **响应**:
  ```json
  {
    "message": "包已成功删除"
  }
  ```

## 错误处理

所有接口在发生错误时会返回以下格式的响应：

```json
{
  "error": "错误信息"
}
```

常见错误码：
- `400`: 请求参数错误
- `401`: 未认证或认证失败
- `403`: 权限不足
- `404`: 资源不存在
- `409`: 资源冲突（如包名已存在）
- `500`: 服务器内部错误

## 使用示例

### 注册新用户

```bash
curl -X POST https://glopm-backend.zeabur.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### 发布包

```bash
curl -X PUT https://glopm-backend.zeabur.app/api/packages/publish \
  -H "x-user-id: YOUR_USER_ID" \
  -H "x-api-key: YOUR_API_KEY" \
  -F "packageName=my-package" \
  -F "version=1.0.0" \
  -F "description=My awesome package" \
  -F "file=@/path/to/file.zip"
```

### 下载包

```bash
curl -O https://glopm-backend.zeabur.app/api/packages/my-package/download/1.0.0
```