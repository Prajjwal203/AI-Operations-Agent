from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ApprovalCreate(BaseModel):
    invoice_id: int
    purchase_order_id: int


class ApprovalDecision(BaseModel):
    reviewer: str
    comments: str | None = None


class ApprovalResponse(BaseModel):
    id: int
    invoice_id: int
    purchase_order_id: int
    status: str
    reviewer: str | None
    comments: str | None
    created_at: datetime
    reviewed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)