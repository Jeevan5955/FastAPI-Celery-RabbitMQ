from bson import ObjectId
from celery import group
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from starlette.responses import JSONResponse
from api import callApi
from celery_tasks.tasks import *
from config.celery_utils import get_task_info
from schemas.schemas import PreprocessingData,ExotelPost
import redis
from database.redis import redisConnection

redisCon= redisConnection()
router = APIRouter(prefix='/dataCollection', tags=['Data Collection'], responses={404: {"description": "Error Occured"}})


@router.post("/exotelPost")
async def exotelPostDetails(exotelPost: ExotelPost):
    """
    Post API data for exotel to get meta data
    """
    eta = datetime.now() + timedelta(minutes=1)
    exotel_meta_data_post.apply_async(kwargs={'data':exotelPost}, eta=eta)
    return JSONResponse({"message": "Exotel Data Recieved"})


@router.get("/exotelGet/")
async def exotelGetDetails(request: Request) -> dict: 
    """
    Get API for exotel to pass through details
    """
    params = dict(request.query_params)
    exotel_meta_data_get.apply_async(args=[params])
    return JSONResponse({"message": "Exotel Data Recieved"})

@router.post("/portDetails/")
async def portDetails(request: Request) -> dict: 
    """
    Post API for bucketization to get port details
    """
    data = await request.json()
    print("portDetails data :",data)
    finalData = []
    for i in data:
        try:
            try:
                totalPorts = int(json.loads(redisCon.get(str(i)+'-'+'portCounter')))
            except:
                totalPorts = 0
            previousPorts = 0 
            if redisCon.get(str(i)+'-'+'previousPorts') == None:
                redisCon.set(str(i)+'-'+'previousPorts', totalPorts)
                finalData.append({'campaignId':i,'port': totalPorts})
            else:
                previousPorts = int(json.loads(redisCon.get(str(i)+'-'+'previousPorts')))
                redisCon.set(str(i)+'-'+'previousPorts', totalPorts)
                finalData.append({'campaignId':i,'port': totalPorts-previousPorts})
        except:
            print("finalData :",finalData)
            return JSONResponse({"ports": []})
            
    print("finalData :",finalData)
    return JSONResponse({"ports": finalData})


