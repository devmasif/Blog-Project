from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.auth_routes import router as auth_router
from routes.post_routes import router as post_router
from routes.comment_routes import router as comment_router
from routes.like_routes import router as likes_router
import uvicorn

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(likes_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
