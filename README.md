# AIFriends - AI 虚拟伙伴对话平台

一个基于大语言模型的 AI 虚拟伙伴平台，支持自定义角色性格与音色，通过语音通话和文字聊天与 AI 角色进行沉浸式互动。

## ✨ 功能特性

- **角色创建与分享** — 自定义角色头像、背景图、名字、性格简介，并选择专属音色
- **流式文字聊天** — 基于 SSE（Server-Sent Events）实现 AI 回复的实时流式输出
- **语音合成（TTS）** — 聊天过程中 AI 回复同步合成语音，实现语音通话体验
- **语音识别（ASR）** — 支持语音输入，将语音实时转为文字
- **语音活动检测（VAD）** — 基于 Silero VAD 模型，智能检测语音输入起止
- **Function Call** — AI 角色可调用工具函数（如获取当前时间、查询知识库）
- **知识库** — 基于 LanceDB 向量数据库 + LangChain 实现 RAG 检索增强生成
- **对话记忆** — 自动维护与每个角色的长期对话记忆
- **用户系统** — 注册、登录、个人资料管理，JWT Token 认证
- **首页广场** — 浏览所有用户分享的 AI 角色

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **前端框架** | Vue 3 + Vite |
| **UI 组件** | Tailwind CSS 4 + DaisyUI 5 |
| **状态管理** | Pinia |
| **路由** | Vue Router |
| **后端框架** | Django 6 + Django REST Framework |
| **数据库** | SQLite |
| **认证** | Simple JWT（Access + Refresh Token） |
| **大模型框架** | LangChain + LangGraph |
| **大模型** | 阿里云百炼 Qwen（通义千问） |
| **语音合成** | 阿里云 CosyVoice TTS（WebSocket 双工流式） |
| **语音识别** | 阿里云百炼 ASR |
| **语音检测** | Silero VAD（ONNX Runtime Web） |
| **向量数据库** | LanceDB |
| **Embedding** | 阿里云 text-embedding-v4 |

## 📁 项目结构

```
AIFriends/
├── backend/                    # Django 后端
│   ├── backend/                # Django 配置
│   │   ├── settings.py         # 项目设置
│   │   ├── urls.py             # 主路由
│   │   └── wsgi.py / asgi.py
│   ├── web/                    # 主应用
│   │   ├── models/             # 数据模型
│   │   │   ├── user.py         # 用户资料模型
│   │   │   ├── character.py    # 角色 & 音色模型
│   │   │   └── friend.py       # 好友 & 消息 & 系统提示词模型
│   │   ├── views/              # 视图层
│   │   │   ├── user/           # 用户注册/登录/登出/Token刷新
│   │   │   ├── create/         # 角色创建/更新/删除/列表
│   │   │   ├── friend/         # 好友管理 & 消息聊天 & ASR
│   │   │   ├── homepage/       # 首页广场
│   │   │   └── profile/        # 个人资料更新
│   │   ├── documents/          # 知识库模块
│   │   │   ├── utils/          # 文档切分 & 自定义 Embedding
│   │   │   ├── lancedb_storage/# LanceDB 向量存储
│   │   │   └── data.txt        # 知识库原始数据
│   │   └── migrations/         # 数据库迁移
│   ├── media/                  # 用户上传文件（头像、背景图）
│   ├── static/frontend/        # Vite 构建产物
│   ├── .env                    # 环境变量配置
│   └── manage.py
├── fronted/                    # Vue 前端
│   ├── src/
│   │   ├── components/         # 公共组件（角色卡片、导航栏）
│   │   ├── views/              # 页面视图
│   │   │   ├── homepage/       # 首页
│   │   │   ├── friend/         # 好友列表
│   │   │   ├── create/         # 角色创建 & 更新
│   │   │   └── user/           # 登录/注册/个人空间
│   │   ├── js/                 # API 请求封装 & 工具函数
│   │   ├── stores/             # Pinia 状态管理
│   │   └── router/             # Vue Router 路由配置
│   ├── package.json
│   └── vite.config.js
└── main.py
```

## 🚀 快速开始

### 环境要求

- **Python** 3.13+
- **Node.js** 20.19+ 或 22.12+
- **阿里云百炼 API Key**（用于大模型、TTS、ASR、Embedding）

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd AIFriends
```

### 2. 后端配置

```bash
# 创建并激活虚拟环境
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
pip install langchain langchain-openai langchain-community langgraph langchain-text-splitters
pip install lancedb openai websockets pillow python-dotenv

# 配置环境变量（见下方 .env 说明）

# 执行数据库迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 启动后端服务
python manage.py runserver
# 后端运行在 http://127.0.0.1:8000
```

#### 环境变量配置

编辑 `backend/.env` 文件，填入你的阿里云百炼 API Key：

```env
API_KEY="你的阿里云百炼API Key"
API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1"
WSS_URL="wss://dashscope.aliyuncs.com/api-ws/v1/inference"
VOICE_URL="https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
```

### 3. 前端配置

```bash
# 新开一个终端
cd fronted

# 安装依赖
npm install

# 启动开发服务器
npm run dev
# 前端运行在 http://127.0.0.1:5173
```

### 4. 生产构建

```bash
cd fronted
npm run build
# 打包产物自动输出到 backend/static/frontend/
# 然后通过 Django 统一提供服务
```

### 5. 初始化数据（必须）

项目启动后，需要通过 Django Admin 后台添加以下基础数据，否则部分功能无法正常使用：

#### 添加音色数据

1. 访问 `http://127.0.0.1:8000/admin/`，使用超级管理员账号登录
2. 进入 **Voice** 管理页面，添加音色记录
3. 每条记录需填写：
   - `name`：音色显示名称（如"温柔女声"）
   - `voice_id`：阿里云 CosyVoice 音色 ID（如 `longxiaochun`、`longxiaoxia` 等，参考[阿里云官方文档](https://help.aliyun.com/document_detail/2712195.html)）

#### 添加系统提示词

1. 进入 **SystemPrompt** 管理页面，添加提示词记录
2. 系统提示词分为两类，通过 `title` 字段区分：
   - `title = "回复"`：用于对话回复的角色扮演提示词，定义 AI 的回复风格和行为规则
   - `title = "记忆"`：用于对话记忆摘要的提示词，指导 AI 如何从对话中提取和总结记忆
3. 每条记录需填写：
   - `title`：提示词类型（"回复" 或 "记忆"）
   - `order_number`：排序序号，多条同类型提示词按此字段升序拼接
   - `prompts`：提示词内容

#### 初始化知识库（可选）

如需使用知识库 Function Call 功能，在 Django Shell 中执行：

```bash
python manage.py shell
```

```python
from web.documents.utils.insert_documents import insert_documents
insert_documents()
```

> 注意：执行前需确保 `backend/web/documents/data.txt` 文件存在，且 `.env` 中的 `API_KEY` 已正确配置。

## 🔑 核心架构

### 对话流程

```
用户输入(文字/语音)
    ↓
[ASR 语音识别]（语音输入时）
    ↓
LangGraph Agent
    ↓
┌───────────────┐
│  System Prompt │ ← 角色性格 + 长期记忆 + 近10轮对话
│  LLM (Qwen)   │ ← 流式输出
│  Function Call │ ← 时间查询 / 知识库检索
└───────────────┘
    ↓
┌───────────────┐
│  SSE 流式推送  │ → 前端逐字渲染
│  TTS 语音合成  │ → WebSocket 双工流式 → 前端实时播放
└───────────────┘
    ↓
保存消息 + 更新对话记忆
```

### 认证机制

- 使用 JWT（Access Token + Refresh Token）进行身份认证
- Access Token 有效期 2 小时，Refresh Token 有效期 7 天
- 前端 axios 拦截器自动处理 Token 刷新，401 时透明刷新并重试请求

### 对话记忆机制

系统采用 **自动摘要记忆** 机制，由独立的 LangGraph Agent 负责：

- 每次对话结束后，系统会将**原始记忆** + **最近 10 轮对话**发送给记忆 Agent
- 记忆 Agent 根据"记忆"类型的系统提示词，自动提取和总结关键信息
- 生成的记忆摘要保存在 `Friend.memory` 字段中
- 下次对话时，记忆摘要作为上下文注入到 System Prompt 中，实现跨会话的长期记忆

### 数据模型关系

```
User (Django内置)
 └── UserProfile (1:1)
      ├── Character (1:N) — 用户创建的 AI 角色
      │    └── Voice (N:1) — 关联的音色
      └── Friend (1:N) — 用户的好友关系
           ├── Character (N:1)
           ├── Message (1:N) — 聊天记录
           └── memory — 长期记忆摘要（TextField）
```

### API 接口一览

| 模块 | 方法 | 接口路径 | 说明 | 认证 |
|------|------|---------|------|------|
| 用户 | POST | `/api/user/account/register/` | 用户注册 | ✗ |
| 用户 | POST | `/api/user/account/login/` | 用户登录 | ✗ |
| 用户 | POST | `/api/user/account/logout/` | 用户登出 | ✓ |
| 用户 | POST | `/api/user/account/refresh_token/` | 刷新 Token | ✗ |
| 用户 | GET | `/api/user/account/get_user_info/` | 获取用户信息 | ✓ |
| 资料 | POST | `/api/user/profile/update/` | 更新个人资料 | ✓ |
| 角色 | POST | `/api/create/character/create/` | 创建角色 | ✓ |
| 角色 | POST | `/api/create/character/update/` | 更新角色 | ✓ |
| 角色 | GET | `/api/create/character/get_single/` | 获取单个角色 | ✓ |
| 角色 | GET | `/api/create/character/get_list/` | 获取角色列表 | ✗ |
| 角色 | POST | `/api/create/character/remove/` | 删除角色 | ✓ |
| 音色 | GET | `/api/create/voice/get_list/` | 获取音色列表 | ✓ |
| 好友 | GET | `/api/friend/get_list` | 获取好友列表 | ✓ |
| 好友 | POST | `/api/friend/get_or_create/` | 获取或创建好友 | ✓ |
| 好友 | POST | `/api/friend/remove` | 删除好友 | ✓ |
| 聊天 | POST | `/api/friend/message/chat` | 发送消息（SSE流式） | ✓ |
| 聊天 | GET | `/api/friend/message/get_history` | 获取聊天历史 | ✓ |
| ASR | POST | `/api/friend/message/asr/asr` | 语音识别 | ✓ |
| 首页 | GET | `/api/homepage/index/` | 首页角色广场 | ✗ |

## 📝 注意事项

1. 需要在阿里云百炼平台申请 API Key，并确保账户有足够额度
2. 语音通话功能需要角色绑定音色（通过管理后台添加音色数据）
3. 知识库功能需先执行文档导入初始化 LanceDB
4. 开发环境前后端分别运行在不同端口，已配置 CORS 跨域
5. 生产环境需修改 `SECRET_KEY`、设置 `DEBUG=False`，配置 `ALLOWED_HOSTS`

## 📄 License

MIT
