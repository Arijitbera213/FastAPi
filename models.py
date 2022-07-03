import datetime
import string
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from pydantic import BaseModel

# Define To Do class inheriting from Base
class ToDo(BaseModel):
    __tablename__ = 'TradeDetails'
    id = Column(Integer, primary_key=True, index=True)
    buySellIndicator = Column(String,  index=True)
    price = Column(float)
    quantity = Column(Integer, default=True)
class ToDo1(BaseModel):
    __tablename__ = 'Trade'
    id = Column(Integer, primary_key=True, index=True)
    assest_class = Column(String, index=True)
    counterparty = Column(String, index=True)
    instrument_id = Column(String, index=True)
    instrument_name = Column(String)
    trade_date_time=Column(datetime, index=True)
    trade_details = relationship("User", back_populates="TradeDetails")
    trade_id=Column(String, primary_key=True )
    trader=Column(String, index=True)
