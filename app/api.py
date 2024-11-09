from fastapi import FastAPI

# from app.forums.reddit.router import router as reddit_router
# from app.forums.stackoverflow.router import router as stackoverflow_router
# import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return "Forum ai API"


# app.include_router(reddit_router, prefix="/api")
# app.include_router(stackoverflow_router, prefix="/api")
