import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.users import user_router
from routes.movies import movie_router
from database.connection import conn

app = FastAPI()

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(movie_router, prefix="/movie")


@app.on_event("startup")
def on_startup():
	conn()

@app.get("/")
async def home():
    return RedirectResponse(url="/movie/")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
