import json
from urllib import request

from app.config import LLM_API_BASE, LLM_API_KEY, LLM_MODEL


def build_ticket_text(ticket: dict) -> str:
    return f"{ticket['title']}\n{ticket['description']}"


def rule_based_analysis(title: str, description: str) -> dict:
    text = f"{title} {description}".lower()

    if any(word in text for word in ["退款", "退货", "refund", "退费"]):
        category = "refund"
        department = "after_sales"
        priority = "high"
    elif any(word in text for word in ["破损", "坏", "无法使用", "质量", "损坏"]):
        category = "quality"
        department = "quality_team"
        priority = "high"
    elif any(word in text for word in ["物流", "快递", "配送", "没收到", "延迟"]):
        category = "logistics"
        department = "logistics_team"
        priority = "medium"
    elif any(word in text for word in ["发票", "开票", "invoice"]):
        category = "invoice"
        department = "finance"
        priority = "medium"
    elif any(word in text for word in ["账号", "登录", "密码", "账户"]):
        category = "account"
        department = "support"
        priority = "medium"
    else:
        category = "general"
        department = "support"
        priority = "normal"

    if any(word in text for word in ["投诉", "紧急", "马上", "严重", "威胁"]):
        priority = "urgent"

    summary = f"客户反馈：{title}。建议由 {department} 处理，优先级为 {priority}。"
    return {
        "category": category,
        "priority": priority,
        "department": department,
        "ai_summary": summary,
        "analysis_type": "mock_rules",
    }


def build_reply(ticket: dict) -> str:
    customer_name = ticket["customer_name"]
    category = ticket["category"]

    if category == "quality":
        action = "我们会尽快核实商品质量问题，并协助您进行换货或售后处理"
    elif category == "refund":
        action = "我们会核实订单和售后条件，并协助您推进退款或退货流程"
    elif category == "logistics":
        action = "我们会联系物流侧核查配送状态，并同步后续处理进展"
    elif category == "invoice":
        action = "我们会核对开票信息，并协助您处理发票相关问题"
    elif category == "account":
        action = "我们会协助您排查账号或登录问题"
    else:
        action = "我们会尽快核实您反馈的问题，并安排对应人员跟进"

    return (
        f"{customer_name}您好，已收到您的反馈。{action}。"
        "给您带来的不便我们深感抱歉，后续处理结果会尽快同步给您。"
    )


def build_analysis_prompt(ticket: dict) -> str:
    return (
        "你是售后客服工单助手。请根据工单内容判断 category、priority、department，"
        "并给出一句简短 summary。只输出 JSON。\n\n"
        f"工单标题：{ticket['title']}\n"
        f"工单描述：{ticket['description']}\n"
    )


def build_reply_prompt(ticket: dict) -> str:
    return (
        "你是售后客服助手。请根据工单内容生成一段礼貌、保守、可执行的客服回复建议。"
        "不要承诺无法确认的赔偿或时效。\n\n"
        f"客户：{ticket['customer_name']}\n"
        f"分类：{ticket['category']}\n"
        f"优先级：{ticket['priority']}\n"
        f"问题：{ticket['title']} - {ticket['description']}\n"
    )


def call_llm(prompt: str) -> str:
    url = f"{LLM_API_BASE.rstrip('/')}/chat/completions"
    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def analyze_ticket(ticket: dict) -> dict:
    fallback = rule_based_analysis(ticket["title"], ticket["description"])
    if not LLM_API_KEY:
        return fallback

    try:
        raw = call_llm(build_analysis_prompt(ticket))
        fallback["ai_summary"] = raw
        fallback["analysis_type"] = "llm_with_rule_fields"
        return fallback
    except Exception:
        fallback["analysis_type"] = "mock_rules_after_llm_error"
        return fallback


def suggest_reply(ticket: dict) -> dict:
    fallback = build_reply(ticket)
    if not LLM_API_KEY:
        return {"suggested_reply": fallback, "reply_type": "mock_template"}

    try:
        return {"suggested_reply": call_llm(build_reply_prompt(ticket)), "reply_type": "llm"}
    except Exception:
        return {"suggested_reply": fallback, "reply_type": "mock_template_after_llm_error"}
