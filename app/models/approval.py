from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, func
)
from app.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    purchase_order_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=False
    )

    status = Column(String(30), default="pending", nullable=False)

    reviewer = Column(String(150), nullable=True)

    comments = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    reviewed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )