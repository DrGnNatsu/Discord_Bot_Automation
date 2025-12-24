from fastapi import Depends

from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService


# 1. Injectable Repository
def get_user_repo() -> UserRepository:
    return UserRepository()


# 2. Injectable Service (Depends on Repo)
def get_auth_service(
        user_repo: UserRepository = Depends(get_user_repo)
) -> AuthService:
    return AuthService(user_repo=user_repo)