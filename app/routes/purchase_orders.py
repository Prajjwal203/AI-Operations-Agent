from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.purchase_order import PurchaseOrder


router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])


class PurchaseOrderCreate(BaseModel):
    po_number: str = Field(min_length=1, max_length=100)
    vendor_name: str = Field(min_length=1, max_length=255)
    order_date: date
    total_amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class PurchaseOrderResponse(PurchaseOrderCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


@router.post("/", response_model=PurchaseOrderResponse, status_code=201)
def create_purchase_order(
    po_data: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    po = PurchaseOrder(**po_data.model_dump())
    db.add(po)

    try:
        db.commit()
        db.refresh(po)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Purchase order number already exists."
        )

    return po


@router.get("/", response_model=list[PurchaseOrderResponse])
def get_purchase_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).order_by(
        PurchaseOrder.id.desc()
    ).all()


@router.get("/{po_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(po_id: int, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == po_id
    ).first()

    if not po:
        raise HTTPException(
            status_code=404,
            detail="Purchase order not found."
        )

    return po