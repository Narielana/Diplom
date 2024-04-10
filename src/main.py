from fastapi import FastAPI
from src.routes import ping as ping_routes
from src.routes import user as user_routes


app = FastAPI()

app.include_router(ping_routes.router)
app.include_router(user_routes.router)
