from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.approval import Approval
from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder
from app.services.invoice_comparison import compare_invoice_with_po


def create_approval(
    invoice_id: int,
    purchase_order_id: int,
    db: Session
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise ValueError("Invoice not found.")

    purchase_order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == purchase_order_id
    ).first()

    if not purchase_order:
        raise ValueError("Purchase order not found.")

    comparison = compare_invoice_with_po(
        invoice_id, purchase_order_id, db
    )

    if comparison["status"] != "matched":
        raise ValueError(
            "Invoice has discrepancies and cannot enter the approval workflow."
        )

    approval = Approval(
        invoice_id=invoice_id,
        purchase_order_id=purchase_order_id,
        status="pending"
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return approval


def decide_approval(
    approval_id: int,
    decision: str,
    reviewer: str,
    comments: str | None,
    db: Session
):
    approval = db.query(Approval).filter(
        Approval.id == approval_id
    ).first()

    if not approval:
        raise ValueError("Approval not found.")

    if approval.status != "pending":
        raise ValueError("This approval has already been decided.")

    if decision not in ["approved", "rejected"]:
        raise ValueError("Invalid approval decision.")

    approval.status = decision
    approval.reviewer = reviewer
    approval.comments = comments
    approval.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(approval)

    return approval