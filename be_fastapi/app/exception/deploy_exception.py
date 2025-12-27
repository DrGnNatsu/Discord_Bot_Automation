from starlette import status

from app.exception.base_exception import AppException


class UserCreateFailException(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to create user"


class NoWorkflowFoundException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "No workflow found in the provided script"


class CompilationFailedException(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to compile workflow script"
    
    def __init__(self, detail: str = None):
        super().__init__()
        if detail:
            self.detail = f"Failed to compile workflow script: {detail}"