from fastapi import HTTPException, status
from ..auth import get_password_hash, verify_password, create_access_token
from ..schemas.users import UserCreate, UserUpdate, User
from ..repositories.UserRepository import UserRepository

class UserController:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: UserCreate) -> User:
        if await self.user_repository.get_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if await self.user_repository.get_by_username(user_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

        hashed_password = get_password_hash(user_data.password)
        
        db_user = await self.user_repository.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        return User.model_validate(db_user)

    async def login_user(self, identifier: str, password: str):
        if "@" in identifier:
            user = await self.user_repository.get_by_email(identifier)
        else:
            user = await self.user_repository.get_by_username(identifier)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user_details(self, current_user: User) -> User:
        user = await self.user_repository.get_by_username(current_user.username)
        if not user:
             raise HTTPException(status_code=404, detail="User not found")
        return User.model_validate(user)

    async def update_user(self, current_user: User, user_update: UserUpdate) -> User:
        user = await self.user_repository.get_by_username(current_user.username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_update.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
        
        updated_user = await self.user_repository.update(user, **update_data)
        return User.model_validate(updated_user)
