from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Integer,
    Numeric,
    String,
    func
)

from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(String(100), unique=True, nullable=False)
    vendor_name = Column(String(255), nullable=False)

    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)

    total_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)

    status = Column(String(30), default="pending", nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )