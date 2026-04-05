from sqlalchemy.orm import Session
from . import models

# USER
def create_user(db: Session, user):
    db_user = models.User(name=user.name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# TRANSACTION
def create_transaction(db: Session, transaction):
    db_tx = models.Transaction(**transaction.dict())
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx


def get_transactions(db: Session):
    return db.query(models.Transaction).all()


def delete_transaction(db: Session, tx_id):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()
    if tx:
        db.delete(tx)
        db.commit()
    return tx