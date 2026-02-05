# Kortix Frontend

基于 Next.js 的 Kortix AI 助手前端应用。

## 功能特性

- 🤖 实时流式对话（SSE）
- 💬 Markdown 消息渲染
- 🎨 暗色/亮色主题自动切换
- 📱 响应式设计
- ⌨️ 键盘快捷键支持

## 技术栈

- Next.js 15+ (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- Radix UI
- React Markdown

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

创建 `.env.local` 文件（已存在）:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
```

### 3. 启动后端服务

确保后端服务已运行在 `http://localhost:8000`：

```bash
cd ../../backend
python start_api.py
```

### 4. 启动开发服务器

```bash
npm run dev
```

打开 [http://localhost:3000](http://localhost:3000) 查看应用。

## 项目结构

```
frontend/
├── app/                    # Next.js App Router 页面
│   ├── globals.css        # 全局样式
│   ├── layout.tsx         # 根布局
│   └── page.tsx           # 主页面
├── components/            # React 组件
│   ├── ui/               # 基础 UI 组件
│   │   ├── button.tsx
│   │   ├── textarea.tsx
│   │   └── scroll-area.tsx
│   └── chat/             # 聊天功能组件
│       ├── chat-container.tsx
│       ├── message-list.tsx
│       ├── message-item.tsx
│       └── message-input.tsx
├── lib/                   # 工具函数
│   ├── api/              # API 客户端
│   │   ├── client.ts
│   │   ├── chat.ts
│   │   ├── history.ts
│   │   └── tools.ts
│   └── utils.ts          # 通用工具
└── types/                # TypeScript 类型定义
    └── api.ts
```

## 功能说明

### 聊天界面

- 输入框支持多行输入
- Enter 发送，Shift+Enter 换行
- 实时流式显示 AI 回复
- Markdown 格式渲染（代码高亮、表格等）
- 自动滚动到最新消息

### API 集成

后端 API 端点：

- `POST /v1/chat` - 流式对话（SSE）
- `POST /v1/chat/reset` - 重置对话
- `GET /v1/history` - 获取历史记录
- `POST /v1/history/save` - 保存历史
- `GET /v1/tools` - 获取工具列表

## 开发命令

```bash
# 开发模式
npm run dev

# 生产构建
npm run build

# 启动生产服务器
npm start

# 代码检查
npm run lint
```

## 注意事项

1. 确保后端服务在启动前端之前已经运行
2. 默认后端地址为 `http://localhost:8000`，可通过环境变量修改
3. 首次运行需要先执行 `npm install` 安装依赖

## 故障排除

### 无法连接到后端

检查：
- 后端服务是否运行在 `http://localhost:8000`
- `.env.local` 中的 API_URL 是否正确
- 浏览器控制台是否有 CORS 错误

### 样式不生效

```bash
# 清除 Next.js 缓存
rm -rf .next
npm run dev
```

## License

MIT
