from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    account_type = Column(String(50), default="基金账户")
    institution = Column(String(100), nullable=True)
    currency = Column(String(10), default="CNY")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    positions = relationship(
        "Position",
        back_populates="account",
        cascade="all, delete-orphan"
    )


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    name = Column(String(150), nullable=False)
    code = Column(String(50), nullable=True)
    asset_type = Column(String(50), default="基金")
    quantity = Column(Float, nullable=True)
    cost_price = Column(Float, nullable=True)
    current_price = Column(Float, nullable=True)
    category = Column(String(50), nullable=True)
    currency = Column(String(10), default="CNY")
    note = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="positions")