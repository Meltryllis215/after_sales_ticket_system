from fastapi import APIRouter, Query

from app.schemas.ticket import TicketCreate, TicketStatusUpdate
from app.services import ticket_service


router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("")
def create_ticket(payload: TicketCreate) -> dict:
    return {"item": ticket_service.create_ticket(payload)}


@router.get("")
def list_tickets(
    status: str | None = Query(default=None),
    category: str | None = Query(default=None),
    priority: str | None = Query(default=None),
) -> dict:
    return {"items": ticket_service.list_tickets(status, category, priority)}


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int) -> dict:
    return {"item": ticket_service.get_ticket(ticket_id)}


@router.patch("/{ticket_id}/status")
def update_status(ticket_id: int, payload: TicketStatusUpdate) -> dict:
    return {"item": ticket_service.update_status(ticket_id, payload.status)}


@router.post("/{ticket_id}/ai/analyze")
def analyze_ticket(ticket_id: int) -> dict:
    return {"item": ticket_service.analyze_and_update(ticket_id)}


@router.post("/{ticket_id}/reply-suggestion")
def generate_reply(ticket_id: int) -> dict:
    return {"item": ticket_service.generate_reply(ticket_id)}
