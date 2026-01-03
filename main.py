import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Controllers.TestController import router as test_router
except ImportError as e:
    print(f"Error importing TestController: {e}")
    # Create a dummy router if import fails
    from fastapi import APIRouter
    test_router = APIRouter()
    @test_router.get("/")
    async def dummy():
        return {{"error": f"Import error: {e}"}}

app = FastAPI(title="Backend API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_router)

@app.get("/")
async def root():
    return {{
        "message": "Backend API is running",
        "status": "ok",
        "swagger": "/docs",
        "api": "/api/test"
    }}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
