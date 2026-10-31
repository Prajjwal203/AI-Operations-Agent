from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, func
from app.database import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)

    po_number = Column(String(100), unique=True, nullable=False)
    vendor_name = Column(String(255), nullable=False)

    order_date = Column(Date, nullable=False)

    total_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)

    status = Column(String(30), default="open", nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )