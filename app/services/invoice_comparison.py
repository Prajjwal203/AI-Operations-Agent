from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder


def compare_invoice_with_po(
    invoice_id: int,
    po_id: int,
    db: Session
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        return {
            "status": "not_found",
            "message": f"Invoice {invoice_id} not found."
        }

    purchase_order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == po_id
    ).first()

    if not purchase_order:
        return {
            "status": "not_found",
            "message": f"Purchase order {po_id} not found."
        }

    discrepancies = []

    if invoice.vendor_name.strip().lower() != purchase_order.vendor_name.strip().lower():
        discrepancies.append({
            "field": "vendor_name",
            "invoice_value": invoice.vendor_name,
            "purchase_order_value": purchase_order.vendor_name
        })

    if invoice.total_amount != purchase_order.total_amount:
        discrepancies.append({
            "field": "total_amount",
            "invoice_value": str(invoice.total_amount),
            "purchase_order_value": str(purchase_order.total_amount)    
        })

    if invoice.currency.upper() != purchase_order.currency.upper():
        discrepancies.append({
            "field": "currency",
            "invoice_value": invoice.currency,
            "purchase_order_value": purchase_order.currency
        })

    if discrepancies:
        return {
            "status": "discrepancy_found",
            "invoice_id": invoice.id,
            "purchase_order_id": purchase_order.id,
            "discrepancies": discrepancies
        }

    return {
        "status": "matched",
        "invoice_id": invoice.id,
        "purchase_order_id": purchase_order.id,
        "message": "Invoice matches the purchase order.",
        "discrepancies": []
    }