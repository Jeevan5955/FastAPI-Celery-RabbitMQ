from bson import ObjectId
from celery import group
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from starlette.responses import JSONResponse
from api import callApi
from celery_tasks.tasks import *
from config.celery_utils import get_task_info
from schemas.schemas import CreateUpdateUser
database = connection()
router = APIRouter(prefix='/user', tags=['User'], responses={404: {"description": "Error Occured"}})

@router.get("/")
async def userGetDetails(request: Request) -> dict: 
    """
    Get API to fetch all the users
    """
    params = dict(request.query_params)
    # exotel_meta_data_get.apply_async(args=[params])
    data = list(database['userinfo'].find({}))
    return JSONResponse({"data": data})

@router.post("/create")
async def userCreateDetails(request: Request):
    """
    Post API data for to create user data
    """
    data = await request.json()
    savingUser.apply_async(args=[data])
    return JSONResponse({"message": "User Data Recieved"})

@router.put("/update")
async def userUpdateDetails(request: Request):
    """
    Put API data for to update user data
    """
    data = await request.json()
    updateUser.apply_async(args=[data])
    return JSONResponse({"message": "Updated User Data"})

@router.patch("/update")
async def userUpdateDetails(request: Request):
    """
    Patch API data for to update user data
    """
    data = await request.json()
    updateUser.apply_async(args=[data])
    return JSONResponse({"message": "Updated User Data"})

@router.delete("/delete")
async def userDeleteDetails(request: Request):
    """
    API data for to delte user data
    """
    data = await request.json()
    deleteUser.apply_async(args=[data])
    return JSONResponse({"message": "Deleted User Data"})




