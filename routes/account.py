from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database.models import Account
from dependencies import SessionDep

router = APIRouter()

@router.post("/")
def create_account(account: Account, session: SessionDep) -> Account:
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get("/")
def read_account(session: SessionDep) -> list[Account]:
    return session.exec(select(Account)).all()


@router.get("/{id}")
def read_account_by_id(id: int, session: SessionDep):
    user = session.exec(select(Account).where(Account.account_id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user