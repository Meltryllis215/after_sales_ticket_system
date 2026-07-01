# GitHub Issues 后续学习路线

说明：本文件只包含智能售后工单处理系统的后续 Issues 规划。当前只是学习路线，不代表已经完成。只有完成并验收后，才可以写进真实简历。

## P0：读懂当前项目

标题：读懂智能售后工单处理系统的业务流程和代码结构

背景：当前项目已经实现工单创建、列表、详情、状态更新、AI mock 分类和回复建议。继续升级前，需要能讲清楚业务流程。

要做什么：

- 阅读 `README.md`、`docs/learning_guide.md`、`docs/resume_and_interview.md`。
- 运行创建工单、查询列表、查询详情、状态更新、AI 分析、回复建议接口。
- 画出工单从创建到关闭的状态流程。
- 写一份 `docs/current_project_notes.md`。

涉及文件：

- `README.md`
- `app/main.py`
- `app/routers/tickets.py`
- `app/schemas/ticket.py`
- `app/services/ticket_service.py`
- `app/services/ai_service.py`
- `app/services/workflow.py`
- `app/database.py`

验收标准：

- 能用 3 分钟讲清楚工单业务流程。
- 能解释规则分类和 mock fallback。
- 能说明为什么它不是完整 Agent。

完成后能否写进简历：不能新增技术点，但能提升面试可解释性。

难度：低

优先级：P0

## P1：补充更完整测试

标题：为智能售后工单处理系统补充更完整的接口和状态流转测试

背景：当前测试只覆盖最小成功路径。后续需要补充非法状态、筛选、404 等基础边界场景。

要做什么：

- 测试非法状态流转返回 400。
- 测试查询不存在工单返回 404。
- 测试按 status/category/priority 筛选。
- 测试退款、物流、发票等不同分类规则。
- 测试无 API key 时回复建议使用 mock template。

涉及文件：

- `tests/test_api.py`
- `app/services/workflow.py`
- `app/services/ai_service.py`
- `app/routers/tickets.py`

验收标准：

- `pytest -q` 全部通过。
- 使用临时 SQLite，不污染正式 `data/tickets.db`。
- 不依赖真实 API key。

完成后能否写进简历：可以写“补充基础接口和状态流转测试”，不要写完整测试体系。

难度：低

优先级：P1

## P2：接真实 LLM API

标题：为售后工单分析和回复建议接入真实 OpenAI 兼容 LLM API

背景：当前 AI 部分无 key 时使用规则和模板，有 key 时预留了调用入口。需要真实验证模型分类和回复建议。

要做什么：

- 配置 `LLM_API_KEY`、`LLM_API_BASE`、`LLM_MODEL`。
- 调用 `/tickets/{id}/ai/analyze`。
- 调用 `/tickets/{id}/reply-suggestion`。
- 记录模型返回不稳定时的 fallback 策略。
- README 增加配置说明。

涉及文件：

- `app/services/ai_service.py`
- `app/services/ticket_service.py`
- `.env.example`
- `README.md`

验收标准：

- 无 key 时 mock 正常。
- 有 key 时真实调用至少成功一次。
- 模型调用失败时 fallback 不影响接口返回。

完成后能否写进简历：可以写“支持配置 OpenAI 兼容接口生成工单分析和回复建议”。

难度：中

优先级：P2

## P3：接真实 embedding

标题：为售后工单增加相似工单检索的 embedding 能力

背景：工单系统当前没有 embedding。后续可以用 embedding 查找历史相似工单，帮助客服参考处理方式。

要做什么：

- 为工单标题和描述生成 embedding。
- 新增相似工单检索 service。
- 提供接口查询相似工单。
- 无 API key 时提供简单关键词 fallback。

涉及文件：

- `app/services/ai_service.py`
- 新增 `app/services/similar_ticket_service.py`
- `app/routers/tickets.py`
- `app/config.py`
- `README.md`

验收标准：

- 创建多个工单后，可以查询相似工单。
- 返回相似工单 id、标题、分类、score。
- 无 key 时仍能 fallback。

完成后能否写进简历：可以写“尝试基于 embedding 做相似工单检索”，前提是真实跑通。

难度：中

优先级：P3

## P4：Chroma/FAISS

标题：为售后工单系统接入 Chroma/FAISS 做相似工单向量检索

背景：相似工单检索如果只靠内存或规则不够真实。Chroma/FAISS 可用于保存工单向量和 metadata。

要做什么：

- 选择 Chroma 或 FAISS。
- 将工单标题、描述、分类写入向量索引。
- 查询相似工单时返回 metadata。
- 支持重建索引。

涉及文件：

- `app/services/similar_ticket_service.py`
- `app/services/ai_service.py`
- `app/routers/tickets.py`
- `requirements.txt`
- `README.md`

验收标准：

- 能创建索引。
- 能查询相似工单。
- 能返回工单来源和 score。

完成后能否写进简历：可以写“使用 Chroma/FAISS 实现相似工单检索练习”。

难度：中高

优先级：P4

## P5：真实 MySQL

标题：为智能售后工单处理系统增加 MySQL 可选运行方式

背景：当前默认 SQLite，只提供 MySQL 表结构。真实 MySQL 能补充后端数据库经验。

要做什么：

- 增加数据库类型配置。
- 连接 MySQL。
- 使用 `schema_mysql.sql` 建表。
- 跑通工单 CRUD、状态更新、AI 分析字段更新。
- 保留 SQLite 默认运行。

涉及文件：

- `app/database.py`
- `app/services/ticket_service.py`
- `app/config.py`
- `schema_mysql.sql`
- `.env.example`
- `README.md`

验收标准：

- SQLite 模式可运行。
- MySQL 模式可完成完整工单流程。
- README 有配置说明。

完成后能否写进简历：可以写“完成 MySQL 版工单 CRUD 练习”，不要写生产级数据库经验。

难度：中

优先级：P5

## P6：简单前端

标题：为智能售后工单处理系统增加简单工单页面

背景：当前只有 API。简单页面可以更直观看到工单创建、列表和回复建议。

要做什么：

- 新增简单 HTML 页面。
- 支持创建工单。
- 支持查看工单列表。
- 支持点击生成回复建议。
- 展示状态和分类结果。

涉及文件：

- `frontend/`
- 或 `app/static/`
- `README.md`

验收标准：

- 页面能打开。
- 能创建工单。
- 能查看列表和回复建议。

完成后能否写进简历：可以写“提供简单页面用于演示工单创建和回复建议”，不要写完整前端项目。

难度：中

优先级：P6

## P7：Docker

标题：为智能售后工单处理系统增加 Docker 本地运行方式

背景：Docker 能提升项目复现能力，方便别人快速启动。

要做什么：

- 编写 `Dockerfile`。
- 编写 `.dockerignore`。
- 支持端口 `8030`。
- README 增加 docker build/run 命令。

涉及文件：

- `Dockerfile`
- `.dockerignore`
- `README.md`

验收标准：

- `docker build` 成功。
- `docker run -p 8030:8030` 后 `/health` 可访问。
- `.env` 和数据库文件不进入镜像。

完成后能否写进简历：可以写“了解 Docker 基础，能为 FastAPI 项目编写简单 Dockerfile”。

难度：中

优先级：P7
