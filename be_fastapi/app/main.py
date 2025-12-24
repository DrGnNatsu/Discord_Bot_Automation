from fastapi import FastAPI

app = FastAPI()

from fastapi import Request
from fastapi.responses import JSONResponse
from app.exception.base_exception import AppException

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


from app.api.v1.endpoints import auth_api




app.include_router(auth_api.router)



