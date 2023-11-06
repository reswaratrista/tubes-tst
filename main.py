import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.users import user_router
from routes.movies import movie_router
from routes.movieCategories import moviecategory_router
from routes.categories import category_router
from routes.histories import history_router
from database.connection import conn

app = FastAPI()

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(movie_router, prefix="/movie")
app.include_router(moviecategory_router, prefix="/moviecategory")
app.include_router(category_router, prefix="/category")
app.include_router(history_router, prefix="/history")


@app.on_event("startup")
def on_startup():
	conn()

@app.get("/")
async def home():
    return RedirectResponse(url="/movie/")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
