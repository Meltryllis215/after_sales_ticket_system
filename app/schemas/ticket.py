from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=80)
    contact: str | None = Field(default=None, max_length=120)
    channel: str = Field(default="web", max_length=40)
    title: str = Field(..., min_length=1, max_length=160)
    description: str = Field(..., min_length=1)


class TicketStatusUpdate(BaseModel):
    status: str = Field(..., min_length=1)
