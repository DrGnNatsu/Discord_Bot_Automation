from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.depends import get_auth_service
from app.db.session import get_db
from app.schemas.login import LoginRequestDTO, LoginResponseDTO
from app.schemas.register import RegisterRequestDTO, RegisterResponseDTO
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponseDTO)
def login(
        form_data: LoginRequestDTO,
        db: Session = Depends(get_db),
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.authenticate_user(login_form=form_data, db=db)


@router.post("/register", response_model=RegisterResponseDTO)
def register(
        form_data: RegisterRequestDTO,
        db: Session = Depends(get_db),
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register_user(register_form=form_data, db=db)
