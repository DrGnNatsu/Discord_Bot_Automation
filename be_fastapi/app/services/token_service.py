import logging
from datetime import timedelta, datetime, timezone

import jwt

from app.core.config import settings

logger = logging.getLogger(__name__)


class TokenService:
    """
    Service for handling all token-related operations including
    JWT token creation, validation, and decoding.
    """

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Create a JWT access token with the provided data and expiration time.
        
        :param data: Dictionary containing claims to encode in the token.
        :param expires_delta: Optional timedelta for token expiration. Defaults to 15 minutes.
        :return: Encoded JWT token string.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)
        
        logger.info(f"Access token created with expiration: {expire}")
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decode and verify a JWT token.
        
        :param token: JWT token string to decode.
        :return: Dictionary containing the decoded token payload.
        :raises jwt.InvalidTokenError: If token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise

    @staticmethod
    def verify_token(token: str) -> bool:
        """
        Verify if a token is valid without decoding it.
        
        :param token: JWT token string to verify.
        :return: True if token is valid, False otherwise.
        """
        try:
            TokenService.decode_token(token)
            return True
        except jwt.InvalidTokenError:
            return False
