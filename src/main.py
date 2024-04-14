from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.routes import ping as ping_routes
from src.routes import user as user_routes
from src.routes import roles as roles_routes


app = FastAPI()


@app.exception_handler(HTTPException)
async def handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )


app.include_router(ping_routes.router)
app.include_router(user_routes.router)
app.include_router(roles_routes.router)
