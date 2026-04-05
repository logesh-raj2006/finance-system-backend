from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    role: str


class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: str
    notes: str