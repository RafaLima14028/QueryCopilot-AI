from fastapi import FastAPI
import uvicorn

from app.middwares.cors import setup_cors

from app.routes.auth import router as router_auth
from app.routes.user import router as router_user


app = FastAPI()


@app.get("/")
def home():
    return {"status": "ok"}


app.include_router(router_auth)
app.include_router(router_user)

setup_cors(app)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        reload=True,
        port=8000
    )
