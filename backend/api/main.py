from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import users, health, scraping

app = FastAPI(
    title="Opta Graph API",
    description="Backend API for Opta Graph application",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発用に全て許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(scraping.router, prefix="/api", tags=["scraping"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)