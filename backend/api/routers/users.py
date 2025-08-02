from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas.user import User, UserCreate, UserUpdate
from api.cruds.user import UserCRUD

router = APIRouter()
user_crud = UserCRUD()

@router.get("/users", response_model=List[User])
async def get_users():
    return user_crud.get_users()

@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    return user_crud.create_user(user)

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    user = user_crud.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    success = user_crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}