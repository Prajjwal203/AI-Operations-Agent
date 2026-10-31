from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder
from app.services.invoice_comparison import compare_invoice_with_po


# Separate temporary database for tests
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(bind=engine)


def setup_function():
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


def create_test_records(db, amount=Decimal("2500.00"),
                        currency="USD", vendor="ABC Technologies"):

    invoice = Invoice(
        invoice_number="INV-TEST-001",
        vendor_name=vendor,
        invoice_date=date(2026, 10, 30),
        total_amount=amount,
        currency=currency
    )

    po = PurchaseOrder(
        po_number="PO-TEST-001",
        vendor_name="ABC Technologies",
        order_date=date(2026, 10, 29),
        total_amount=Decimal("2500.00"),
        currency="USD"
    )

    db.add_all([invoice, po])
    db.commit()

    return invoice.id, po.id


def test_matching_invoice_and_po():
    db = TestingSessionLocal()
    try:
        invoice_id, po_id = create_test_records(db)

        result = compare_invoice_with_po(invoice_id, po_id, db)

        assert result["status"] == "matched"
        assert result["discrepancies"] == []
    finally:
        db.close()


def test_amount_mismatch():
    db = TestingSessionLocal()
    try:
        invoice_id, po_id = create_test_records(
            db, amount=Decimal("2600.00")
        )

        result = compare_invoice_with_po(invoice_id, po_id, db)

        assert result["status"] == "discrepancy_found"
        assert result["discrepancies"][0]["field"] == "total_amount"
    finally:
        db.close()


def test_currency_mismatch():
    db = TestingSessionLocal()
    try:
        invoice_id, po_id = create_test_records(db, currency="EUR")

        result = compare_invoice_with_po(invoice_id, po_id, db)

        assert result["status"] == "discrepancy_found"
        assert result["discrepancies"][0]["field"] == "currency"
    finally:
        db.close()


def test_vendor_mismatch():
    db = TestingSessionLocal()
    try:
        invoice_id, po_id = create_test_records(db, vendor="XYZ Limited")

        result = compare_invoice_with_po(invoice_id, po_id, db)

        assert result["status"] == "discrepancy_found"
        assert result["discrepancies"][0]["field"] == "vendor_name"
    finally:
        db.close()


def test_invoice_not_found():
    db = TestingSessionLocal()
    try:
        result = compare_invoice_with_po(999, 1, db)

        assert result["status"] == "not_found"
    finally:
        db.close()