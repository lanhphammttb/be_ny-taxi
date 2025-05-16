from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        phone_number=user_in.phone_number,
        role=user_in.role,
        password=hashed_password,
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        return None

async def update_user(db: AsyncSession, user: User, user_in: UserUpdate):
    for field, value in user_in.dict(exclude_unset=True).items():
        if field == "password":
            setattr(user, field, get_password_hash(value))
        else:
            setattr(user, field, value)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user: User):
    await db.delete(user)
    await db.commit()
