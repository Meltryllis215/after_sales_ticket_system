# API 测试示例

启动服务：

```powershell
uvicorn app.main:app --reload --port 8030
```

## 健康检查

```powershell
curl.exe "http://127.0.0.1:8030/health"
```

## 创建工单

```powershell
curl.exe -X POST "http://127.0.0.1:8030/tickets" `
  -H "Content-Type: application/json" `
  -d "{\"customer_name\":\"张三\",\"contact\":\"13800000000\",\"channel\":\"web\",\"title\":\"收到商品破损需要处理\",\"description\":\"我昨天收到的耳机外包装破损，右侧耳机无法使用，希望尽快换货。\"}"
```

## 查询工单列表

```powershell
curl.exe "http://127.0.0.1:8030/tickets"
```

按状态筛选：

```powershell
curl.exe "http://127.0.0.1:8030/tickets?status=new"
```

## 查询工单详情

```powershell
curl.exe "http://127.0.0.1:8030/tickets/1"
```

## 更新状态

```powershell
curl.exe -X PATCH "http://127.0.0.1:8030/tickets/1/status" `
  -H "Content-Type: application/json" `
  -d "{\"status\":\"processing\"}"
```

## AI 辅助分类

```powershell
curl.exe -X POST "http://127.0.0.1:8030/tickets/1/ai/analyze"
```

## 客服回复建议

```powershell
curl.exe -X POST "http://127.0.0.1:8030/tickets/1/reply-suggestion"
```
