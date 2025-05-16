from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud import user as crud_user
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get_user_by_username(db, user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = await crud_user.create_user(db, user_in)
    if not user:
        raise HTTPException(status_code=400, detail="Could not create user")
    return user

@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, user_in: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await crud_user.update_user(db, user, user_in)
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await crud_user.delete_user(db, user)
    return
