# Stock-Analyzer

一个用于识别 A 股热点板块的本地可部署项目，包含数据抓取、指标计算、AI 分析（硅基流动），以及 Web UI。

## 快速开始

1) 克隆并安装依赖

```
pip install -r requirements.txt
```

2) 配置环境变量（复制 .env.example 为 .env 并填入密钥）

```
TUSHARE_TOKEN=your_tushare_token
SILICONFLOW_API_KEY=your_siliconflow_api_key
SILICONFLOW_MODEL=your_model_name
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=stock_analyzer
```

3) 启动 API（默认 8000 端口）

```
uvicorn api.app:app --reload
```

4) 启动 Streamlit Web UI（默认使用本地 API）

```
streamlit run web_ui/streamlit_app.py
```

5) 定时任务（可选）

```
python tasks/scheduler.py
```

## 目录结构

```
Stock-Analyzer/
├── api/                 # FastAPI 后端
├── web_ui/              # Streamlit 前端
├── modules/             # 数据获取、指标、AI、DB 工具
├── tasks/               # 定时任务
├── config/              # 配置与环境加载
├── logs/                # 日志目录
├── requirements.txt
└── .env.example
```

## 注意
- `.env` 已加入 `.gitignore`，请勿提交密钥。
- 当前示例使用占位的板块与股票列表，后续可按需替换为真实板块成分。