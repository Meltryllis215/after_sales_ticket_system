import sqlite3

from fastapi import HTTPException

from app.database import get_connection
from app.schemas.ticket import TicketCreate
from app.services.ai_service import analyze_ticket, suggest_reply
from app.services.workflow import can_transition


def row_to_ticket(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "customer_name": row["customer_name"],
        "contact": row["contact"],
        "channel": row["channel"],
        "title": row["title"],
        "description": row["description"],
        "category": row["category"],
        "priority": row["priority"],
        "department": row["department"],
        "status": row["status"],
        "ai_summary": row["ai_summary"],
        "suggested_reply": row["suggested_reply"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def create_ticket(payload: TicketCreate) -> dict:
    analysis = analyze_ticket(
        {
            "title": payload.title,
            "description": payload.description,
            "customer_name": payload.customer_name,
        }
    )
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO tickets (
                customer_name, contact, channel, title, description,
                category, priority, department, status, ai_summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.customer_name,
                payload.contact,
                payload.channel,
                payload.title,
                payload.description,
                analysis["category"],
                analysis["priority"],
                analysis["department"],
                "new",
                analysis["ai_summary"],
            ),
        )
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (cursor.lastrowid,)).fetchone()
    ticket = row_to_ticket(row)
    ticket["analysis_type"] = analysis["analysis_type"]
    return ticket


def list_tickets(status: str | None, category: str | None, priority: str | None) -> list[dict]:
    sql = "SELECT * FROM tickets WHERE 1 = 1"
    params = []
    if status:
        sql += " AND status = ?"
        params.append(status)
    if category:
        sql += " AND category = ?"
        params.append(category)
    if priority:
        sql += " AND priority = ?"
        params.append(priority)
    sql += " ORDER BY id DESC"

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [row_to_ticket(row) for row in rows]


def get_ticket(ticket_id: int) -> dict:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    return row_to_ticket(row)


def update_status(ticket_id: int, status: str) -> dict:
    ticket = get_ticket(ticket_id)
    if not can_transition(ticket["status"], status):
        raise HTTPException(
            status_code=400,
            detail=f"invalid transition from {ticket['status']} to {status}",
        )
    with get_connection() as conn:
        conn.execute(
            "UPDATE tickets SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, ticket_id),
        )
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return row_to_ticket(row)


def analyze_and_update(ticket_id: int) -> dict:
    ticket = get_ticket(ticket_id)
    analysis = analyze_ticket(ticket)
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE tickets
            SET category = ?, priority = ?, department = ?, ai_summary = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                analysis["category"],
                analysis["priority"],
                analysis["department"],
                analysis["ai_summary"],
                ticket_id,
            ),
        )
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    result = row_to_ticket(row)
    result["analysis_type"] = analysis["analysis_type"]
    return result


def generate_reply(ticket_id: int) -> dict:
    ticket = get_ticket(ticket_id)
    reply = suggest_reply(ticket)
    with get_connection() as conn:
        conn.execute(
            "UPDATE tickets SET suggested_reply = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (reply["suggested_reply"], ticket_id),
        )
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    result = row_to_ticket(row)
    result["reply_type"] = reply["reply_type"]
    return result
