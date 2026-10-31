from fastapi import FastAPI
from app.routes.invoices import router as invoice_router
from app.routes.purchase_orders import router as po_router
from app.routes.comparisons import router as comparison_router


app = FastAPI(
    title="AI Operations Agent",
    description="AI-powered business operations automation",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Operations Agent is running!",
        "status": "development"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(invoice_router)

app.include_router(po_router)

app.include_router(comparison_router)