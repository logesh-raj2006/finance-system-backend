from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas, auth

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/transactions")
def create_transaction(transaction: schemas.TransactionCreate, role: str, db: Session = Depends(get_db)):
    if not auth.check_permission(role, "create"):
        raise HTTPException(status_code=403, detail="Permission denied")

    if transaction.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Invalid type")

    return crud.create_transaction(db, transaction)

# READ
@router.get("/transactions")
def get_transactions(role: str, db: Session = Depends(get_db)):
    if not auth.check_permission(role, "view"):
        raise HTTPException(status_code=403, detail="Permission denied")

    return crud.get_transactions(db)

# DELETE
@router.delete("/transactions/{tx_id}")
def delete_transaction(tx_id: int, role: str, db: Session = Depends(get_db)):
    if not auth.check_permission(role, "delete"):
        raise HTTPException(status_code=403, detail="Permission denied")

    tx = crud.delete_transaction(db, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted"}