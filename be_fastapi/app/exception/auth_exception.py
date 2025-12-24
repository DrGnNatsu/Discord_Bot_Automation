from fastapi import status

from app.exception.base_exception import AppException

"""
Login related exceptions
"""


# Case: Auth Failed
class InvalidCredentialsException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


# Case: Permission Denied
class PermissionDeniedException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You do not have permission to access this resource"


# Case: Token Expired
class TokenExpiredException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Your session has expired. Please login again."


"""
Registration related exceptions
"""


# Case: Email Already Registered
class EmailDuplicateException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Email already registered in the system"


# Case: Password Too Weak
class PasswordTooWeakException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The provided password is too weak"


# Case: Password Do Not Match
class PasswordDoNotMatchException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "The provided passwords do not match"