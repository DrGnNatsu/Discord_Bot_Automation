class AppException(Exception):
    """
    Base class for all application errors.
    Each subclass defines its own status_code and detail.
    """
    status_code: int = 500
    detail: str = "An internal error occurred"
    headers: dict =  {"WWW-Authenticate": "Bearer"}

    def __init__(self, detail: str = None, status_code: int = None):
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = status_code