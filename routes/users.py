from fastapi import APIRouter, HTTPException
from sqlmodel import select, or_
from database.models import User, PasswordUpdate
from dependencies import SessionDep

router = APIRouter()

@router.post("/")
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/")
def read_users(session: SessionDep) -> list[User]:
    return session.exec(select(User)).all()


@router.get("/{user_id}")
def read_user_by_id(user_id: int, session: SessionDep):
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{name}")
def read_user_by_name_or_email(name: str, session: SessionDep):
    user = session.exec(
        select(User).where(or_(User.name == name, User.email == name))
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/forgotpassword/{user_id}")
def change_password(user_id: int, password: PasswordUpdate, session: SessionDep):
    user = session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = password.new_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return user