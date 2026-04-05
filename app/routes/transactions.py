from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, schemas, auth, models  
from datetime import date

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

# READ with filtering
@router.get("/transactions")
def get_transactions(
    role: str,
    type: str = Query(None, description="Filter by type: income or expense"),
    category: str = Query(None, description="Filter by category"),
    start_date: date = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: date = Query(None, description="Filter end date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    if not auth.check_permission(role, "view"):
        raise HTTPException(status_code=403, detail="Permission denied")

    query = db.query(models.Transaction)

    if type:
        query = query.filter(models.Transaction.type == type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)

    return query.all()

# DELETE
@router.delete("/transactions/{tx_id}")
def delete_transaction(tx_id: int, role: str, db: Session = Depends(get_db)):
    if not auth.check_permission(role, "delete"):
        raise HTTPException(status_code=403, detail="Permission denied")

    tx = crud.delete_transaction(db, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")

    return {"message": "Deleted"}

# UPDATE
@router.put("/transactions/{tx_id}")
def update_transaction(tx_id: int, transaction: schemas.TransactionCreate, role: str, db: Session = Depends(get_db)):
    if not auth.check_permission(role, "update"):
        raise HTTPException(status_code=403, detail="Permission denied")

    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in transaction.dict().items():
        setattr(tx, key, value)

    db.commit()
    db.refresh(tx)  
    return tx