from sqlmodel import SQLModel, Field, Relationship
from typing import List

# ORM Model
class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True, nullable=False)
    name: str
    email: str
    password: str
    accounts: List["Account"] = Relationship(back_populates="user")

class PasswordUpdate(SQLModel):
    new_password: str

class Account(SQLModel, table=True):
    account_id: int = Field(default=None, primary_key=True, index=True, nullable=False)
    user_id: int = Field(foreign_key="user.user_id")
    account_name: str
    balance: float
    user: "User" = Relationship(back_populates="accounts")
    transactions: List["Transaction"] = Relationship(back_populates="account")

class Category(SQLModel, table=True):
    category_id: int = Field(primary_key=True, index=True, nullable=False)
    category_name: str
    type: str  # income/expense
    transactions: List["Transaction"] = Relationship(back_populates="category")

class Transaction(SQLModel, table=True):
    transaction_id: int = Field(default=None, primary_key=True, index=True, nullable=False)
    user_id: int = Field(foreign_key="user.user_id")  # ยังใช้ ForeignKey แต่ไม่มี Relationship
    account_id: int = Field(foreign_key="account.account_id")
    category_id: int = Field(foreign_key="category.category_id")
    amount: float
    date: str  # YYYY-MM-DD HH:MM:SS
    transaction_type: str  # income/expense
    account: Account = Relationship(back_populates="transactions")
    category: Category = Relationship(back_populates="transactions")

class ExchangeRate(SQLModel, table=True):
    exchange_id: int = Field(primary_key=True, index=True, nullable=False)
    currency_from: str
    currency_to: str
    rate: float
    date: str  # YYYY-MM-DD HH:MM:SS
