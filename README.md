# OnRoad

这是一个用于上下班通勤的小工具，没有什么特别的功能，仅仅是为打工人平淡的生活增加一些波动罢了


## 🚀 特性

- 基于 FastAPI 的高性能异步 API
- 完整的认证和授权系统
- OpenAI 集成支持
- 邮件服务集成
- Sentry 错误监控
- 严格的类型检查和代码质量控制
- 使用 uv 进行高性能依赖管理

## 🛠️ 技术栈

- **Web 框架**: FastAPI 0.114.2+
- **数据验证**: Pydantic v2
- **认证**: JWT, Passlib
- **AI 集成**: OpenAI SDK
- **监控**: Sentry
- **开发工具**:
  - UV: 高性能 Python 包管理器和虚拟环境管理工具
  - Ruff: 代码质量检查
  - MyPy: 静态类型检查
  - Pytest: 单元测试
  - Pre-commit: Git 钩子

## 📦 安装

1. 克隆项目
```bash
git clone [your-repository-url]
cd onroad
```

2. 安装 uv（如果未安装）
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. 安装依赖
```bash
uv sync
```

4. 使用虚拟环境
```bash
# 安装项目依赖
source .venv/bin/activate
```

## 🔧 配置

1. 创建环境变量文件
```bash
cp .env.example .env
```

2. 配置必要的环境变量：
- `OPENAI_API_KEY`: OpenAI API 密钥
- `SECRET_KEY`: JWT 密钥
- `SENTRY_DSN`: Sentry 项目 DSN
- 其他必要的配置项...

## 🚀 运行

1. 启动开发服务器
```bash
fastapi run --reload app/main.py
```

2. 访问 API 文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📝 开发指南

### 代码质量

项目使用多个工具确保代码质量：

1. **类型检查**
```bash
mypy .
```

2. **代码风格检查**
```bash
ruff check .
```

3. **运行测试**
```bash
pytest
```

### Git 提交规范

项目使用 pre-commit 钩子进行提交前检查：

1. 安装 pre-commit
```bash
pre-commit install
```

2. 提交代码时会自动运行检查

## 📁 项目结构

```
onroad/
├── app/                    # 主应用代码
│   ├── api/               # API 路由
│   ├── core/              # 核心功能
│   ├── models/            # 数据模型
│   ├── services/          # 业务服务
│   ├── utils/             # 工具函数
│   ├── exceptions/        # 异常处理
│   ├── main.py           # 应用入口
│   └── __init__.py
├── scripts/               # 工具脚本
├── tests/                 # 测试用例
└── docs/                  # 项目文档
```