# FastAPi_Steeleye



## Installation using cmd

> pip install fastapi

> pip install "uvicorn[standard]"

## What is SQLAlchemy?

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

Read more about[ SQLAlchemy](https://www.sqlalchemy.org/) on their official site.


## File structure
For these examples, let's say you have a directory named my_super_project that contains a sub-directory called sql_app with a structure like this:
.
└── sql_app
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
    
The file _init_.py is just an empty file, but it tells Python that sql_app with all its modules (Python files) is a package.

## Feature

> fetch a trade by id

> fetching a list of trades will need to support searching for trades through the following fields:

- counterparty
- instrumentId
- instrumentName
- trader

> Advanced filtering
The users would now like the ability to filter trades. Your endpoint for fetching a list of trades will need to support filtering using the following optional query parameters:

## Parameter	Description

assetClass	   Asset class of the trade.
end	         The maximum date for the tradeDateTime field.
maxPrice	The maximum value for the tradeDetails.price field.
minPrice	The minimum value for the tradeDetails.price field.
start	The minimum date for the tradeDateTime field.
tradeType	The tradeDetails.buySellIndicator is a BUY or SELL
## Advanced filtering
The users would now like the ability to filter trades. Your endpoint for fetching a list of trades will need to support filtering using the following optional query parameters:

Parameter	Description
assetClass	Asset class of the trade.
end	The maximum date for the tradeDateTime field.
maxPrice	The maximum value for the tradeDetails.price field.
minPrice	The minimum value for the tradeDetails.price field.
start	The minimum date for the tradeDateTime field.
tradeType	The tradeDetails.buySellIndicator is a BUY or SELL
All maximum and minimum fields are inclusive (e.g. minPrice=2&maxPrice=10 will return 2 <= tradeDetails.price <= 10).


## Implement support for pagination on the list of trades.

## Create the SQLAlchemy parts¶
Let's refer to the file sql_app/database.py.

## Import the SQLAlchemy parts¶

The import of create_engine, declarative_base and sessionmaker were done.
The create_engine() function produces an Engine object based on a URL.
>from sqlalchemy import create_engine

The declarative_base() base class contains a MetaData object where newly defined Table objects are collected.
>from sqlalchemy.ext.declarative import declarative_base

Session class is defined using sessionmaker() – a configurable session factory method which is bound to the engine object created earlier.
>from sqlalchemy.orm import sessionmaker

>SQLALCHEMY_DATABASE_URL = "sqlite:///./TODDOO.db"


## Create a database URL for SQLAlchemy

This is the entire working of database.py 

```sh
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

>The import of the files has been made

SQLALCHEMY_DATABASE_URL = 'sqlite:///./steeleye.db'

>The database URI that should be used for the connection.

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

```


## Create the database models¶

Let's now see the file sql_app/models.py.

Create SQLAlchemy models from the Base class¶
We will use this Base class we created before to create the SQLAlchemy models.


```sh
from sqlalchemy import Column, Integer, ForeignKey ,String, Float, Boolean,DateTime 

>As known the Column, Integer, ForeignKey ,String, Float, Boolean,DateTime  are the part of data types which are used in SQL as well

from sqlalchemy.orm import relationship

> It provides a relationship between two mapped classes.


from database import Base

>database design philosophy that prizes Availability over Consistency of operations. 

>Two differents are created below one is tradedetails and the other one is trade with various properties inside

class TradeDetails(Base):
    _tablename_ = "trade_details"

    id = Column(String, primary_key=True, index=True)
    buySellIndicator = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    trades = relationship("Trade", back_populates='trade_details')


class Trade(Base):
    _tablename_ = "trade"

    asset_class = Column(String)
    counterparty = Column(String)
    instrument_id = Column(Integer)
    instrument_name = Column(String)
    trade_date_time = Column(DateTime)
    trade_details_id = Column(String, ForeignKey("trade_details.id"))
    trade_details = relationship("TradeDetails", back_populates='trades')
    trade_id = Column(String, primary_key=True, index=True)
    trader = Column(String)

```


## Create the Pydantic models¶
Now let's check the file sql_app/schemas.py.


### Create initial Pydantic models / schemas¶

>Create an trade and tradedetails Pydantic models (or let's say "schemas") to have common attributes while creating or reading data and create an trade and tradedetails that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.

>So, the user will also have a password when creating it.

*But for security, the password won't be in other Pydantic models, for example, it won't be sent from the API when reading a user*

---

```sh
import datetime as dt

from typing import Optional , List
from pydantic import BaseModel, Field

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")

    price: float = Field(description="The price of the Trade.")

    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")

    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")

    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")

    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")

    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")

    trade_details: List[TradeDetails] = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")

    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")

    trader: str = Field(description="The name of the Trader")

```

## CRUD utils¶

Now let's see the file sql_app/crud.py.

In this file we will have reusable functions to interact with the data in the database.

>CRUD comes from: Create, Read, Update, and Delete.

...although in this example we are only creating and reading.

### Read data¶
Import Session from sqlalchemy.orm, this will allow you to declare the type of the db parameters and have better type checks and completion in your functions.


>Import models (the SQLAlchemy models) and schemas (the Pydantic models / schemas).


#### Create utility functions to:

- Read a single user by ID and by email.
- Read multiple users.
- Read multiple items.

#### Create data¶

Now create utility functions to create data.

The steps are:

- Create a SQLAlchemy model instance with your data.
- add that instance object to your database session.
- commit the changes to the database (so that they are saved).
- refresh your instance (so that it contains any new data from the database, like the generated ID).

---

```sh
from sqlalchemy.orm import Session

from import models, schemas


def get_trade_by_id(db: Session, trade_id: str):
    return db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()

def get_trade(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trade).offset(skip).limit(limit).all()

def create_trade(db: Session, trade: schemas.Trade):
    db_trade = models.Trade(
        asset_class=trade.asset_class,
        counterparty=trade.counterparty,
        instrument_id=trade.instrument_id,
        instrument_name=trade.instrument_name,
        trade_date_time=trade.trade_date_time,
        trade_id=trade.trade_id,
        trader=trade.trader
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trade(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trade).offset(skip).limit(limit).all()

def create_trade_details(db: Session, trade_details: schemas.TradeDetails,trade_id: str):
    
    db_trade_details = models.TradeDetails(
        owner_id=trade_id,
        buySellIndicator=trade_details.buySellIndicator,
        price=trade_details.price,
        quantity=trade_details.quantity,
    )
    db.add(db_trade_details)
    db.commit()
    db.refresh(db_trade_details)
    return db_trade_details
```

## Main FastAPI app¶
And now in the file sql_app/main.py let's integrate and use all the other parts we created before.

*Create the database tables¶*

In a very simplistic way create the database tables:

---

```sh
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException,Request,Response
from sqlalchemy.orm import Session
import schemas, models # noqa: E402

from database import SessionLocal,engine



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


@app.get("/trades")
async def get_trades(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.Trade).limit(limit).all()


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

```

## Create a dependency¶
Now use the SessionLocal class we created in the sql_app/database.py file to create a dependency.

We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.

And then a new session will be created for the next request.

For that, we will create a new dependency with yield, as explained before in the section about Dependencies with yield.

Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request, and then close it once the request is finished.

---

```sh
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException,Request,Response
from sqlalchemy.orm import Session
import schemas, models # noqa: E402

from database import SessionLocal,engine



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

---

# Dependency

---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/trades")
async def get_trades(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.Trade).limit(limit).all()


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
```
---

## Check it¶
You can copy this code and use it as is.

Info

In fact, the code shown here is part of the tests. As most of the code in these docs.

Then you can run it with Uvicorn:

```sh
uvicorn sql_app.main:app --reload
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)


And then, you can open your browser at http://127.0.0.1:8000/docs.

And you will be able to interact with your FastAPI application, reading data from a real database:

## Interact with the database directly¶
If you want to explore the SQLite database (file) directly, independently of FastAPI, to debug its contents, add tables, columns, records, modify data, etc. you can use DB Browser for SQLite.

It will look like this:
![image](https://user-images.githubusercontent.com/56600106/177052291-92cfdda4-87dd-47e5-a534-9e2aecee1aeb.png)
![image](https://user-images.githubusercontent.com/56600106/177052297-f9c1d3b6-11ae-4e31-b3be-04dda8a95228.png)
![image](https://user-images.githubusercontent.com/56600106/177052303-8a944fac-f656-4b0d-ad48-65be510ac388.png)
![image](https://user-images.githubusercontent.com/56600106/177052308-621ece45-82cb-4b7b-bd33-bc33c0b7cae3.png)
![image](https://user-images.githubusercontent.com/56600106/177052314-7660115d-481e-4af5-b7f2-a5f772e1866d.png)
![image](https://user-images.githubusercontent.com/56600106/177052331-619540b6-485b-4287-91b3-9bca8b4668af.png)
![image](https://user-images.githubusercontent.com/56600106/177052337-c4461f09-e22e-40e5-ad2a-a5c22bc5b3af.png)
![image](https://user-images.githubusercontent.com/56600106/177052340-eaa55a7e-d0cd-4344-b7fc-f02fdbb31851.png)
![image](https://user-images.githubusercontent.com/56600106/177052359-8768a939-0183-4b13-8c1e-c3e49430c084.png)
![image](https://user-images.githubusercontent.com/56600106/177052361-b10587c6-ee51-4447-bd80-8a39d375a75a.png)
![image](https://user-images.githubusercontent.com/56600106/177052373-06e37216-a365-49be-915d-f49a8245e85a.png)
![image](https://user-images.githubusercontent.com/56600106/177052375-4baa50ab-0f5a-4fee-9914-3a7351090d71.png)
![image](https://user-images.githubusercontent.com/56600106/177052398-31d91026-1606-458e-9b36-8be35e788220.png)
![image](https://user-images.githubusercontent.com/56600106/177052400-e166ca2a-1081-4266-bf42-17079039f0b9.png)
![image](https://user-images.githubusercontent.com/56600106/177052439-cd97a21b-8dd6-4c7d-908d-52ee809403d0.png)
![image](https://user-images.githubusercontent.com/56600106/177052448-7b15201f-9172-4a14-a403-2cc2f753731c.png)
![image](https://user-images.githubusercontent.com/56600106/177052476-c8817617-b44a-40fb-a463-2d39f16db088.png)
![image](https://user-images.githubusercontent.com/56600106/177052482-2cec591b-c96c-42f5-955e-d41396cab302.png)
![image](https://user-images.githubusercontent.com/56600106/177052491-ee764976-6fea-4cf1-87e0-607d336d753b.png)
![image](https://user-images.githubusercontent.com/56600106/177052496-82d6e4da-9d62-49be-99c8-a6b8f64c6156.png)
![image](https://user-images.githubusercontent.com/56600106/177081412-9289c1ba-09e0-4421-a698-ffcab2b6f880.png)
![image](https://user-images.githubusercontent.com/56600106/177081460-2107c10f-0286-4063-b227-0d1596989a0b.png)
![image](https://user-images.githubusercontent.com/56600106/177081477-bbeab382-2881-4ad5-a3d5-ce372878254f.png)
![image](https://user-images.githubusercontent.com/56600106/177081494-bf825a1a-98e0-4825-813f-62c5decc71f3.png)



