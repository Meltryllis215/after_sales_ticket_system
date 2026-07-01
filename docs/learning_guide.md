# 学习指南

## 这个项目练什么

- FastAPI 路由和请求体
- SQLite CRUD
- 业务字段建模
- 工单状态流转
- AI mock fallback
- Prompt 和回复建议
- MySQL 表结构阅读

## 推荐阅读顺序

1. `README.md`
2. `app/main.py`
3. `app/routers/tickets.py`
4. `app/schemas/ticket.py`
5. `app/services/ticket_service.py`
6. `app/services/ai_service.py`
7. `app/services/workflow.py`
8. `app/database.py`
9. `docs/api_examples.md`

## 业务流程

```text
客户提交问题
  -> 创建工单
  -> 规则/LLM 辅助分类
  -> 设置分类、优先级、处理部门
  -> 客服查看工单
  -> 更新处理状态
  -> 生成回复建议
  -> 关闭工单
```

## 你需要能讲清楚

1. 为什么工单需要状态。
2. 为什么创建工单时自动分类。
3. 分类、优先级、处理部门分别有什么用。
4. mock fallback 为什么重要。
5. SQLite 和 MySQL 的区别。
6. 这个项目为什么不是 Agent。
