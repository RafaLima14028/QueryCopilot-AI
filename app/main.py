from fastapi import FastAPI
import uvicorn

from app.middwares.cors import setup_cors

from app.routes.auth import router as router_auth


app = FastAPI()

app.include_router(router_auth)

setup_cors(app)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        reload=True,
        port=8000
    )
