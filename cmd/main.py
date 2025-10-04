import uvicorn
from fastapi import FastAPI, Depends
from internal.server.controllers import router
from settings.env import settings
from settings.logger import setup_logging
from internal.server.middleware import setup_middlewares
from internal.repository.order.order_manager import OrderManager
from internal.services.order import OrderService
from internal.domain.contracts.order import OrderServiceInterface
from internal.repository.db.postgres.connection import get_db
from sqlalchemy.orm import Session

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

setup_middlewares(app)

def get_order_service(db: Session = Depends(get_db)) -> OrderServiceInterface:
    repo = OrderManager(db)
    return OrderService(repo)

app.dependency_overrides[OrderServiceInterface] = get_order_service

app.include_router(router)

@app.get("/")
def root():
    return {"service": settings.APP_NAME, "version": settings.APP_VERSION}

if __name__ == "__main__":
    uvicorn.run(
        "cmd.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL,
    )
