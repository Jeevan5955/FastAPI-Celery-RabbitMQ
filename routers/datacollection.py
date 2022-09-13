from bson import ObjectId
from celery import group
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from starlette.responses import JSONResponse
from api import callApi
from celery_tasks.tasks import *
from config.celery_utils import get_task_info
from schemas.schemas import PreprocessingData,ExotelPost

router = APIRouter(prefix='/dataCollection', tags=['Data Collection'], responses={404: {"description": "Error Occured"}})


@router.post("/exotelPost")
async def exotelPostDetails(exotelPost: ExotelPost):
    """
    Post API data for exotel to get meta data
    """
    eta = datetime.now() + timedelta(minutes=1)
    exotel_meta_data_post.apply_async(kwargs={'data':ExotelPost}, eta=eta)
    return JSONResponse({"message": "Exotel Data Recieved"})


@router.get("/exotelGet/")
async def exotelGetDetails(request: Request) -> dict: 
    """
    Get API for exotel to pass through details
    """
    params = request.query_params
    exotel_meta_data_get.apply_async(args=[params])
    return JSONResponse({"message": "Exotel Data Recieved"})


