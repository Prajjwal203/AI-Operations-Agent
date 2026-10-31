from app.database import Base, engine
from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder
from app.models.approval import Approval


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()