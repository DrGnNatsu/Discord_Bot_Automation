from fastapi import Depends

from app.repositories.user_repo import UserRepository
from app.repositories.workflow_repo import WorkflowRepository
from app.services.auth_service import AuthService
from app.services.token_service import TokenService
from fastapi.security import OAuth2PasswordBearer

# 1. Injectable Repository
def get_user_repo() -> UserRepository:
    return UserRepository()

def get_workflow_repo() -> WorkflowRepository:
    return WorkflowRepository()


# 2. Injectable Service (Depends on Repo)
def get_token_service() -> TokenService:
    return TokenService()

def get_auth_service(
        user_repo: UserRepository = Depends(get_user_repo),
        token_service: TokenService = Depends(get_token_service)
) -> AuthService:
    return AuthService(user_repo=user_repo, token_service=token_service)

# 3. Check login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token_service: TokenService = Depends(get_token_service),
        token: str = Depends(oauth2_scheme)
):
    payload = token_service.decode_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise Exception("Invalid token: missing subject claim")
    return user_id

