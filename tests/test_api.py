import importlib
import sys

from fastapi.testclient import TestClient


def load_test_client(monkeypatch, tmp_path) -> TestClient:
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "tickets_test.db"))
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    for module_name in list(sys.modules):
        if module_name == "app" or module_name.startswith("app."):
            del sys.modules[module_name]

    main = importlib.import_module("app.main")
    return TestClient(main.app)


def test_health_ticket_crud_ai_and_reply(monkeypatch, tmp_path):
    client = load_test_client(monkeypatch, tmp_path)

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["message"] == "after sales ticket system is running"
    assert health.json()["llm_enabled"] is False

    created = client.post(
        "/tickets",
        json={
            "customer_name": "测试客户",
            "contact": "test-contact",
            "channel": "web",
            "title": "商品破损需要换货",
            "description": "收到的耳机外包装破损，右侧耳机无法使用，希望换货。",
        },
    )
    assert created.status_code == 200
    ticket = created.json()["item"]
    ticket_id = ticket["id"]
    assert ticket["category"] == "quality"
    assert ticket["priority"] == "high"
    assert ticket["status"] == "new"
    assert ticket["analysis_type"] == "mock_rules"

    listed = client.get("/tickets")
    assert listed.status_code == 200
    assert len(listed.json()["items"]) == 1

    detail = client.get(f"/tickets/{ticket_id}")
    assert detail.status_code == 200
    assert detail.json()["item"]["title"] == "商品破损需要换货"

    status = client.patch(f"/tickets/{ticket_id}/status", json={"status": "processing"})
    assert status.status_code == 200
    assert status.json()["item"]["status"] == "processing"

    analysis = client.post(f"/tickets/{ticket_id}/ai/analyze")
    assert analysis.status_code == 200
    assert analysis.json()["item"]["analysis_type"] == "mock_rules"

    reply = client.post(f"/tickets/{ticket_id}/reply-suggestion")
    assert reply.status_code == 200
    reply_item = reply.json()["item"]
    assert reply_item["reply_type"] == "mock_template"
    assert "已收到您的反馈" in reply_item["suggested_reply"]
