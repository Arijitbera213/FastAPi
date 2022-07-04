from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException,Request,Response,Query
from sqlalchemy.orm import Session
import schemas, models # noqa: E402
import datetime as dt
from datetime import datetime
from datetime import *
from database import SessionLocal,engine

from sqlalchemy import desc


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/trades")
async def get_trades(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.Trade).limit(limit).all()
@app.get("/trades_details")
async def get_tradesDetails(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.TradeDetails).limit(limit).all()

@app.post("/trade")
async def create_trade(trades: schemas.Trade, db: Session = Depends(get_db)):
    db_trade=db.query(models.Trade).filter(models.Trade.trade_id == trades.trade_id).first()
    if db_trade:
        raise HTTPException(status_code=400, detail="Trade already exists")
    new_trade = models.Trade(trade_id=trades.trade_id, trader=trades.trader, asset_class=trades.asset_class,
                             counterparty=trades.counterparty, trade_date_time=trades.trade_date_time,
                             instrument_id=trades.instrument_id, instrument_name=trades.instrument_name)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade

@app.post("/trade_details/{id}")
async def create_trade_details(trade_details: schemas.TradeDetails, id: str, db: Session = Depends(get_db)):
    new_trade_details = models.TradeDetails(id=id, buySellIndicator=trade_details.buySellIndicator,
                                            price=trade_details.price, quantity=trade_details.quantity)
    db.add(new_trade_details)
    db.commit()
    db.refresh(new_trade_details)
    return new_trade_details

@app.get("/trade/{trade_id}")
async def get_trade_by_id(trade_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()
    
@app.get("/trade/{counterparty}/details")
async def get_trade_by_counterparty(counterparty: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.counterparty == counterparty).all()

@app.get("/trade/{trader}/details")
async def get_trade_by_trader(trader: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.trader == trader).all()


@app.get("/trade/{instrument_id}/details")
async def get_trade_by_instrument_id(instrument_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.instrument_id == instrument_id).all()

@app.get("/trade/{instrument_name}/details")
async def get_trade_by_instrument_name(instrument_name: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.instrument_name == instrument_name).all()

@app.get("/trade/{assetClass}/{end}/{maxPrice}/{minPrice}/{start}/{tradetype}")
def Advanced_filtering(assetClass: Optional[str], end: Optional[dt.datetime], maxPrice: Optional[float], minPrice: Optional[float], start: Optional[dt.datetime], tradetype: Optional[str], db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.asset_class == assetClass).filter(models.Trade.trade_date_time >= start).filter(models.Trade.trade_date_time <= end).filter(models.TradeDetails.price <= maxPrice).filter(models.TradeDetails.price >= minPrice).filter(models.Trade.trader == tradetype).all()

@app.get("/tradequantity/")
def SortingDESC( db: Session = Depends(get_db)):
    return db.query(models.TradeDetails).order_by(models.TradeDetails.quantity.desc())


def get_data(db: Session, page: int = 0, limit: int = 50):
    # Note not the best option for large data sets.
    try:
        data = db.query(models.Trade).offset(page).limit(limit).all()
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail='There was an error while processing your request.')
@app.get('/pagination')
def Pagination(db: Session = Depends(get_db), page: int = 0, limit: int = 50):
    return get_data(db=db, page=page, limit=limit)
