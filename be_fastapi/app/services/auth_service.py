import logging
from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.exception.auth_exception import InvalidCredentialsException, \
    PasswordTooWeakException, PasswordDoNotMatchException
from app.repositories.user_repo import UserRepository
from app.schemas.login import LoginResponseDTO, LoginRequestDTO
from app.schemas.register import RegisterRequestDTO, RegisterResponseDTO, RegisterCreateUserDTO
from app.utils.auth import verify_password, create_access_token, is_password_valid, get_password_hash

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    """
    Authenticate user and generate JWT token upon successful login.
    :param login_form: LoginRequestDTO containing user login credentials.
    :param db: Database session.    
    :return: LoginResponseDTO containing JWT token and user role.
    :raises UserNotFoundException: If the user with the provided email does not exist.
    :raises InvalidCredentialsException: If the provided password is incorrect. 
    """

    def authenticate_user(self, login_form: LoginRequestDTO, db: Session) -> LoginResponseDTO:
        user = self.user_repo.get_user_by_email(login_form.email, db)

        # Verify password and user existence
        if not user or not verify_password(login_form.password, user.password_hash):
            raise InvalidCredentialsException

        data: dict = {
            "sub": str(user.id),
            "role": user.role.value
        }
        expires_delta: timedelta = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOUR)

        access_token = create_access_token(data=data, expires_delta=expires_delta)

        return LoginResponseDTO(
            jwt_token=access_token,
            role=user.role # type: ignore
        )

    """
    Create the user 
    :param register_form: RegisterRequestDTO containing user register credentials
    :param db: Database session.    
    :return: RegisterResponseDTO containing messages.
    """

    def register_user(self, register_form: RegisterRequestDTO, db: Session) -> RegisterResponseDTO:
        # Silent Failure
        if self.user_repo.get_user_by_email(register_form.email, db):
            logger.info(f"Registration attempt for existing email: {register_form.email}")

            return RegisterResponseDTO(message="User registered successfully")

        if not is_password_valid(register_form.password):
            raise PasswordTooWeakException

        if register_form.password != register_form.confirm_password:
            raise PasswordDoNotMatchException

        data: RegisterCreateUserDTO = RegisterCreateUserDTO(
            email=register_form.email,
            password=get_password_hash(register_form.password)
        )

        self.user_repo.create_user(data=data, db=db)

        return RegisterResponseDTO(message="User registered successfully")