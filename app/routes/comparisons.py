from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.invoice_comparison import compare_invoice_with_po

router = APIRouter(prefix="/comparisons", tags=["Comparisons"])


@router.get("/invoice/{invoice_id}/purchase-order/{po_id}")
def compare_invoice(
    invoice_id: int,
    po_id: int,
    db: Session = Depends(get_db)
):
    return compare_invoice_with_po(invoice_id, po_id, db)