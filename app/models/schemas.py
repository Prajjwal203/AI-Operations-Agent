from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class InvoiceCreate(BaseModel):
    invoice_number: str = Field(min_length=1, max_length=100)
    vendor_name: str = Field(min_length=1, max_length=255)
    invoice_date: date
    due_date: date | None = None
    total_amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    vendor_name: str
    invoice_date: date
    due_date: date | None
    total_amount: Decimal
    currency: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)