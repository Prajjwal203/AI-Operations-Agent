from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.approval import Approval

from app.database import get_db
from app.models.approval_schemas import (
    ApprovalCreate,
    ApprovalDecision,
    ApprovalResponse
)
from app.services.approval_service import (
    create_approval,
    decide_approval
)

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.post("/", response_model=ApprovalResponse, status_code=201)
def submit_for_approval(
    data: ApprovalCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_approval(
            data.invoice_id,
            data.purchase_order_id,
            db
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{approval_id}/decision", response_model=ApprovalResponse)
def review_approval(
    approval_id: int,
    data: ApprovalDecision,
    decision: str,
    db: Session = Depends(get_db)
):
    try:
        return decide_approval(
            approval_id,
            decision,
            data.reviewer,
            data.comments,
            db
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[ApprovalResponse])
def get_approval_history(db: Session = Depends(get_db)):
    approvals = (
        db.query(Approval)
        .order_by(Approval.created_at.desc())
        .all()
    )

    return approvals
