from starlette import status

from app.exception.base_exception import AppException


class UserCreateFailException(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to create user"