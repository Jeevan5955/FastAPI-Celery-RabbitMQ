import time

import uvicorn as uvicorn
from fastapi import FastAPI

from config.celery_utils import create_celery
from routers import datacollection
from dotenv import dotenv_values

config = dotenv_values(".env")

def create_app() -> FastAPI:
    current_app = FastAPI(title="Asynchronous tasks processing with Celery and RabbitMQ",
                          description="FastAPI Application for Data Collection "
                                      "driven architecture with Celery and RabbitMQ",
                          version="1.0.0", )

    current_app.celery_app = create_celery()
    current_app.include_router(datacollection.router)
    return current_app


app = create_app()
celery = app.celery_app

@app.on_event("startup")
def startup_event():
    print("config :",config)

@app.on_event("shutdown")
async def shutdown_event():
    print("Server shutdown")
    pass

@app.middleware("http")
async def add_process_time_header(request, call_next):
    print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=int(config['PORT']), reload=True)
