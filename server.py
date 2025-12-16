"""Start the Marlene API server with FastAPI."""
import uvicorn
from backend.config import settings


if __name__ == "__main__":
    uvicorn.run(
        "backend.api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
