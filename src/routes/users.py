from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..schemas.users import UserCreate, UserLogin, UserUpdate, User, Token
from ..schemas.users import User as UserSchema
from ..controllers.users import UserController
from ..dependencies import get_user_controller
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["Users"])

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    controller: UserController = Depends(get_user_controller),
):
    return await controller.register_user(user_data)

@router.post("/users/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    controller: UserController = Depends(get_user_controller),
):
    return await controller.login_user(form_data.username, form_data.password)

@router.get("/user", response_model=User)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    controller: UserController = Depends(get_user_controller),
):
    return await controller.get_current_user_details(current_user)

@router.put("/user", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    controller: UserController = Depends(get_user_controller),
):
    return await controller.update_user(current_user, user_update)
