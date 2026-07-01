# 智能售后工单处理系统

一个面向实习简历的小型 FastAPI 后端项目，用来练习 Python 后端、CRUD、业务流程建模、状态流转、AI 辅助分类和客服回复建议生成。

项目定位是“贴近企业业务的小型后端系统”，不是生产级客服平台，也不是完整 Agent。

## 功能列表

- 工单创建：录入客户、联系方式、渠道、标题和问题描述。
- 工单列表：支持按状态、分类、优先级筛选。
- 工单详情：查看完整工单信息。
- 状态流转：支持 `new`、`processing`、`waiting_customer`、`resolved`、`closed`。
- AI 辅助分类：判断分类、优先级和处理部门。
- 客服回复建议：根据工单内容生成保守回复建议。
- mock fallback：无 API key 时使用规则分类和模板回复。
- SQLite 默认运行：本地无需安装数据库。
- MySQL SQL：提供后续迁移表结构。

## 技术栈

- Python
- FastAPI
- Pydantic
- SQLite
- RESTful API
- 规则分类
- Prompt 组织
- OpenAI-compatible API fallback

## 项目结构

```text
after_sales_ticket_system/
  app/
    main.py
    config.py
    database.py
    routers/
      tickets.py
    schemas/
      ticket.py
    services/
      ticket_service.py
      ai_service.py
      workflow.py
  docs/
    api_examples.md
    learning_guide.md
    resume_and_interview.md
  schema_mysql.sql
  requirements.txt
  README.md
```

## 安装

```powershell
cd after_sales_ticket_system
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

如果你已有装好 FastAPI 的环境，也可以直接使用已有环境运行。

## 运行

```powershell
uvicorn app.main:app --reload --port 8030
```

启动后访问：

- `http://127.0.0.1:8030/docs`
- `http://127.0.0.1:8030/health`

## 快速测试

创建工单：

```powershell
curl.exe -X POST "http://127.0.0.1:8030/tickets" `
  -H "Content-Type: application/json" `
  -d "{\"customer_name\":\"张三\",\"contact\":\"13800000000\",\"channel\":\"web\",\"title\":\"收到商品破损需要处理\",\"description\":\"我昨天收到的耳机外包装破损，右侧耳机无法使用，希望尽快换货。\"}"
```

查看列表：

```powershell
curl.exe "http://127.0.0.1:8030/tickets"
```

更新状态：

```powershell
curl.exe -X PATCH "http://127.0.0.1:8030/tickets/1/status" `
  -H "Content-Type: application/json" `
  -d "{\"status\":\"processing\"}"
```

AI 分类：

```powershell
curl.exe -X POST "http://127.0.0.1:8030/tickets/1/ai/analyze"
```

生成回复建议：

```powershell
curl.exe -X POST "http://127.0.0.1:8030/tickets/1/reply-suggestion"
```

更多接口示例见 [docs/api_examples.md](docs/api_examples.md)。

## 可选 LLM API

默认不需要 API key。没有 key 时，系统用规则分类和模板回复。

如需调用 OpenAI 兼容接口：

```powershell
$env:LLM_API_KEY="your-api-key"
$env:LLM_API_BASE="https://api.openai.com/v1"
$env:LLM_MODEL="gpt-4o-mini"
uvicorn app.main:app --reload --port 8030
```

不要把真实 key 写进代码或提交到 GitHub。

## 项目边界

本项目没有实现：

- 登录和权限
- 前端页面
- 高并发
- 微服务
- 生产级部署
- 完整 Agent
- 多轮对话
- 模型训练或微调
- 真实客服系统对接

## 简历表述

智能售后工单处理系统｜FastAPI + AI 辅助分类业务项目

- 基于 FastAPI 实现售后工单处理后端，支持工单创建、列表查询、详情查看、状态更新和 SQLite 持久化。
- 设计工单状态流转和字段模型，包含分类、优先级、处理部门、AI 摘要和客服回复建议。
- 实现规则驱动的 AI mock fallback，可根据工单描述判断售后分类、优先级和处理部门；配置 API key 后预留 OpenAI 兼容接口调用入口。
- 通过项目练习 Python 后端 CRUD、业务流程建模、Prompt 组织和客服场景下的 AI 辅助处理。
