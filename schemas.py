from datetime import datetime
from pydantic import BaseModel

# Create ToDo Schema (Pydantic Model)
class ToDo1Create(BaseModel):
    assest_class :str
    counterparty :str
    instrument_id :str
    instrument_name :str
    trade_date_time:datetime
    trade_id:str
    trader:str

# Complete ToDo Schema (Pydantic Model)
class ToDo1(BaseModel):
    id: int
    assest_class :str
    counterparty :str
    instrument_id :str
    instrument_name :str
    trade_date_time:datetime
    trade_id:str
    trader:str

    class Config:
        orm_mode = True
class ToDoCreate(BaseModel):
    buySellIndicator: str
    price: float
    quantity: int

# Complete ToDo Schema (Pydantic Model)
class ToDo(BaseModel):
    id: int
    buySellIndicator: str
    price: float
    quantity: int

    class Config:
        orm_mode = True