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
    # 1. Check whether the invoice exists
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise ValueError("Invoice not found.")

    # 2. Check whether the purchase order exists
    purchase_order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == purchase_order_id
    ).first()

    if not purchase_order:
        raise ValueError("Purchase order not found.")

    # 3. Prevent duplicate pending approvals
    existing_approval = db.query(Approval).filter(
        Approval.invoice_id == invoice_id,
        Approval.purchase_order_id == purchase_order_id,
        Approval.status == "pending"
    ).first()

    if existing_approval:
        raise ValueError(
            "A pending approval already exists for this invoice and purchase order."
        )

    # 4. Compare invoice with purchase order
    comparison = compare_invoice_with_po(
        invoice_id, purchase_order_id, db
    )

    if comparison["status"] != "matched":
        raise ValueError(
            "Invoice has discrepancies and cannot enter the approval workflow."
        )

    # 5. Create approval record
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