from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="投资提升之路·独立复盘系统",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "investment-review-system",
        "version": "0.1.0"
    }


@app.get("/api/accounts", response_model=list[schemas.AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(models.Account).all()


@app.post("/api/accounts", response_model=schemas.AccountOut)
def create_account(
    data: schemas.AccountCreate,
    db: Session = Depends(get_db)
):
    account = models.Account(**data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@app.get("/api/positions", response_model=list[schemas.PositionOut])
def list_positions(db: Session = Depends(get_db)):
    return db.query(models.Position).all()


@app.post("/api/positions", response_model=schemas.PositionOut)
def create_position(
    data: schemas.PositionCreate,
    db: Session = Depends(get_db)
):
    account = db.query(models.Account).filter(
        models.Account.id == data.account_id
    ).first()

    if not account:
        raise HTTPException(
            status_code=404,
            detail="账户不存在，请先创建账户"
        )

    position = models.Position(**data.model_dump())
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


@app.put("/api/positions/{position_id}", response_model=schemas.PositionOut)
def update_position(
    position_id: int,
    data: schemas.PositionCreate,
    db: Session = Depends(get_db)
):
    position = db.query(models.Position).filter(
        models.Position.id == position_id
    ).first()

    if not position:
        raise HTTPException(status_code=404, detail="持仓不存在")

    if not db.query(models.Account).filter(
        models.Account.id == data.account_id
    ).first():
        raise HTTPException(status_code=404, detail="账户不存在")

    for key, value in data.model_dump().items():
        setattr(position, key, value)

    db.commit()
    db.refresh(position)
    return position


@app.delete("/api/positions/{position_id}")
def delete_position(
    position_id: int,
    db: Session = Depends(get_db)
):
    position = db.query(models.Position).filter(
        models.Position.id == position_id
    ).first()

    if not position:
        raise HTTPException(status_code=404, detail="持仓不存在")

    db.delete(position)
    db.commit()
    return {"message": "持仓已删除"}