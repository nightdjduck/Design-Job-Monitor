# 设计岗位监控系统

这是一个自动监控多个公司招聘页面，当有新的设计岗位发布时，通过 Telegram 发送通知的系统。

## 功能特点

- 🔍 自动监控 7 家公司的招聘页面
- 🎨 智能识别设计相关岗位（Design, UI/UX, Visual Design 等）
- 📱 通过 Telegram 实时通知
- 💾 记录已检测的岗位，避免重复通知
- ⏰ 可配置的检查间隔

## 监控的公司

1. Airbnb - https://careers.airbnb.com/positions/?_offices=china
2. OpenAI - https://openai.com/careers/search/?c=f6aa76fa-ec6f-4dd8-b3c7-531e313e3e63
3. Binance - https://www.binance.com/en/careers/department?name=Product%20%26%20Design&team=Design&job=
4. Bitget - https://hire-r1.mokahr.com/social-recruitment/bitget/100000079#/jobs?zhineng%5B0%5D=100004123
5. Bybit - https://jobs.bybitglobal.com/social-recruitment/bybit/45685#/jobs?department%5B0%5D=1110472
6. Ethena.fi - https://x.com/ethena_labs/jobs

## 安装步骤

### 1. 克隆或下载项目

```bash
cd design-job-monitor
```

### 2. 安装依赖

推荐使用虚拟环境：

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 配置 Telegram Bot

#### 创建 Telegram Bot

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 命令
3. 按照提示设置机器人名称和用户名
4. 获取 Bot Token（格式类似：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

#### 获取 Chat ID

1. 在 Telegram 中搜索 `@userinfobot`
2. 发送任意消息，获取你的 Chat ID（数字格式，如：`123456789`）

### 4. 配置环境变量

复制 `.env.example` 文件为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```env
TELEGRAM_BOT_TOKEN=你的_bot_token
TELEGRAM_CHAT_ID=你的_chat_id
CHECK_INTERVAL_MINUTES=60
```

## 使用方法

### 运行监控程序

本地运行一次：
```bash
python main.py
```

本地循环监控（每小时检查一次）：
```bash
python main.py --loop
```

## 部署到 GitHub Actions（推荐）

本项目已配置 GitHub Actions，可以实现云端自动运行，无需本地挂机。

### 部署步骤

1. **Fork 本项目** 到你的 GitHub 账号。

2. **配置 Secrets**：
   - 进入项目仓库 -> `Settings` -> `Secrets and variables` -> `Actions`
   - 点击 `New repository secret`
   - 添加以下两个 Secret：
     - `TELEGRAM_BOT_TOKEN`: 你的 Bot Token
     - `TELEGRAM_CHAT_ID`: 你的 Chat ID

3. **启用 Workflow**：
   - 进入 `Actions` 标签页
   - 第一次可能需要点击 "I understand my workflows, go ahead and enable them"
   - 可以手动触发一次 `Design Job Monitor` 来测试

### 自动运行机制

- 程序配置为每小时自动运行一次。
- 每次运行后，如果有新的岗位记录，会自动提交更新 `jobs_data.json` 到仓库，确保不会重复通知。
- 运行日志可以在 Actions 页面查看。

## 配置说明

按 `Ctrl+C` 停止监控

## 配置说明

### 环境变量

- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token（必需）
- `TELEGRAM_CHAT_ID`: Telegram Chat ID（必需）
- `CHECK_INTERVAL_MINUTES`: 检查间隔（分钟），默认 60

### 关键词配置

可以在 `config.py` 中修改设计岗位的关键词：

```python
"keywords": ["design", "designer", "ui", "ux", "visual", "graphic", "product design"]
```

## 数据存储

程序会在 `jobs_data.json` 文件中记录已检测到的岗位，避免重复通知。该文件会自动创建和管理。

## 注意事项

1. 首次运行会检测所有岗位，可能会收到较多通知
2. 某些网站可能有反爬虫机制，如果抓取失败，请检查网络连接
3. 建议在服务器或长期运行的机器上运行此程序
4. 可以使用 `screen` 或 `tmux` 在后台运行程序

## 故障排除

### Telegram 通知不工作

- 检查 `.env` 文件中的 Token 和 Chat ID 是否正确
- 确保 Bot Token 有效
- 确保已向 Bot 发送过消息（某些 Bot 需要先启动对话）

### 抓取失败

- 检查网络连接
- 某些网站可能需要更长的超时时间
- 可以尝试增加 `scraper.py` 中的超时时间

## 许可证

MIT License

# Design-Job-Monitor
