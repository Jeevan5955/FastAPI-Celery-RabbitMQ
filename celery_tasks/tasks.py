from typing import List
from celery import shared_task
from api import callApi
from bson import ObjectId
from database.database import connection
import json
from datetime import datetime, timedelta
import requests
import redis
import xmltodict
from azure.storage.blob import BlockBlobService, PublicAccess

database = connection()


def distribution_of_data(data):
    data["talkTime"] = int(data["talkTime"])*1000
    data["ringingTime"] = int(data["ringingTime"])*1000
    saving_data_to_completeCallingInfo.apply_async(args=[data])
    if data["systemDisposition"] == "CONNECTED":
        saving_audio_to_azure_new.apply_async(args=[data["customerCRTId"], data["recordingFileUrl"]])
    else:
        pass
  

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='dataCollection:Exotel Meta Data Post.')
def exotel_meta_data_post(self,data):
    print("Post Data recieved :",data)
    POOL = redis.ConnectionPool(host='redis.saarthi.ai', port=6379,password='sAaRtH1at2o22')
    r = redis.StrictRedis(connection_pool=POOL, charset="utf-8", decode_responses=True)
    customerData = json.loads(r.get(str(data.CallSid)))
    callDetails ="https://945749771aab3393aab60e37d119d4f9d123d98b9960f8a1:f2c692871cd51a8d38f169c56856754a287c79f13f728090@api.exotel.com/v1/Accounts/saarthi3/Calls/"+data['CallSid']+"?details=true"
    r = requests.get(url=callDetails)
    info = xmltodict.parse(r.text)
    postCallData = info['TwilioResponse']['Call']
    print("Details true data :",postCallData)
    newdata = {}
    if postCallData['Status'] == "completed":
        newdata['systemDisposition'] = "CONNECTED"
        try:
            newdata['talkTime'] =  postCallData['Details']['Legs']['Leg']['OnCallDuration']
        except:
            newdata['talkTime'] =  postCallData['Details']['ConversationDuration']
    else:
        newdata['systemDisposition'] = postCallData['Status']
        newdata['talkTime'] =  0
    newdata['ringingTime'] =  0
    newdata['callType'] = "Outbound"
    newdata['recordingFileUrl'] = postCallData['RecordingUrl']
    newdata['customerCRTId'] = data['CallSid']
    newdata['sessionId'] = data['CallSid']
    newdata['client_details'] = customerData['clientName']
    newdata["dstPhone"] = postCallData['From']
    newdata["srcPhone"] = postCallData['To']
    newdata["phone"] = postCallData['From']
    newdata["dialedTime"] = postCallData['StartTime']
    if (customerData['callId'] != None):
        newdata['customerId'] = customerData['callId']
    else:
        newdata['customerId'] = "0"
    newdata["campaignId"] = "123"
    print("Post Data final :",newdata)
    
    print("Inside preprocessingCode")
    telephonyDetails = list(database["telephonydetails"].find({'sessionId':data.CallSid}))
    if len(telephonyDetails) >= 0:
        pass
    else:
        distribution_of_data(newdata)
        database["telephonydetails"].insert_one(newdata)
    
    return { "message": "Meta Data Recieved" }


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='dataCollection:Exotel Meta Data Get.')
def exotel_meta_data_get(self,data):
    print("Pass through Data recieved :",data)
    
    POOL = redis.ConnectionPool(host='redis.saarthi.ai', port=6379,password='sAaRtH1at2o22')
    r = redis.StrictRedis(connection_pool=POOL, charset="utf-8", decode_responses=True)
    postCallData = data
    customerData = json.loads(r.get(postCallData['CallSid']))
    newdata = {}
    if (postCallData['Stream[Status]'] == "completed" or postCallData['Stream[Status]'] == "in-progress" ):
        newdata['systemDisposition'] = "CONNECTED"
    else:
        newdata['systemDisposition'] = postCallData['Stream[Status]']

    
    newdata['ringingTime'] =  postCallData['Leg1RingingDuration']
    if (postCallData['Stream[Duration]'] != None):
        newdata['talkTime'] =  postCallData['Stream[Duration]']
    else:
      newdata['talkTime'] = 0
    
    newdata['callType'] = "Outbound"
    newdata['recordingFileUrl'] = postCallData['Stream[RecordingUrl]']
    newdata['customerCRTId'] = postCallData['CallSid']
    newdata['sessionId'] = postCallData['CallSid']
    newdata['client_details'] = customerData['clientName']
    newdata["dstPhone"] = postCallData['CallFrom']
    newdata["srcPhone"] = postCallData['CallTo']
    newdata["phone"] = postCallData['CallFrom']
    newdata["dialedTime"] = postCallData['StartTime']
    if (customerData['callId'] != None):
      newdata['customerId'] = customerData['callId']
    else:
      newdata['customerId'] = "0"
    newdata["campaignId"] = "123"
    print("Exotel Meta Data Get :", newdata)
    telephonyDetails = list(database["telephonydetails"].find({'sessionId':data.CallSid}))
    if len(telephonyDetails) >= 0:
        print("Inside pass through exists")
        pass
    else:
        print("Inside pass through Not exists")
        distribution_of_data(newdata)
        database["telephonydetails"].insert_one(newdata)

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='dataCollection:Saving data to Complete Calling Info')
def saving_data_to_completeCallingInfo(self,data):
    print("Inside saving_data_to_completeCallingInfo :",data)
    try:
        if str(data['customerId']) == "0":
            print("check")
            pass
        else:
            print("inside")
            print("Data :",data)
            if data['client_details'].find('Testing') == -1:
                URL = "https://connectors.saarthi.ai/campaign/api/campaignManagement/completeCallingInfo/v1/create" 
            else:
                URL = "https://staging-connectors.saarthi.ai/campaign/api/campaignManagement/completeCallingInfo/v1/create" 
            headers = {'content-type': 'application/json'}
            if data['systemDisposition'] == "CONNECTED":
                data["connectionStatus"] = "Connected"
            else:
                data["connectionStatus"] = "Not Connected"
            if data['systemDisposition'] == "Failed" or data['systemDisposition'] == "failed":
                data['systemDisposition'] == "NA"
            else:
                pass
            
            body = {
                'callingId': str(data['customerId']),
                "information":{
                    'phone_number':str(data['dstPhone']),
                    'disposition':data['systemDisposition'],
                    'talk_time':data['talkTime'],
                    'ring_time':data['ringingTime'],
                    'telephonyId':data['campaignId'],
                    'dialed_time':data['dialedTime'],
                    'srcPhone':data['srcPhone'],
                    'callType':data['callType'],
                    'created_at':str(datetime.now().isoformat())[0:23]+"Z",
                    'sessionId':data['customerCRTId'],
                    'connectionStatus':data['connectionStatus']
                }
                
            }
            print("URL :",URL)
            print("Data sent to complete calling info :", body)
            r = requests.post(url=URL, data=json.dumps(body), headers=headers)
            print("Creating Conversation :", r.json())
    except Exception as e:
        print("Czentrix Saving data to MongoDB :",e)


@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
             name='recordingSaving:Saving audio to azure.')
@shared_task(name='Saving audio to azure')
def saving_audio_to_azure_new(self,sessionId, recordingFileUrl):
    r = requests.get(url=recordingFileUrl)
    try:
        if r.status_code in ['500',500,'502',502]:
            saving_audio_to_azure_new.delay(sessionId, recordingFileUrl)
        else:
            block_blob_service = BlockBlobService(account_name="saarthistorage", account_key="IC7/YcmMOIadVgkhxNvXErJN4gJ7rmC+Mzvz5NkIWbYKXVvy7DoHHOP7w0JY5CURlHwndy8WsQ+LDl7VKDjkDw==;EndpointSuffix=core.windows.net")
            container_name = "ameyocalls"

            response = requests.get(str(recordingFileUrl), stream=True)
            block_blob_service.create_blob_from_stream(container_name, str(sessionId)+'.mp3', response.raw)
    except Exception as e:
        block_blob_service = BlockBlobService(account_name="saarthistorage", account_key="IC7/YcmMOIadVgkhxNvXErJN4gJ7rmC+Mzvz5NkIWbYKXVvy7DoHHOP7w0JY5CURlHwndy8WsQ+LDl7VKDjkDw==;EndpointSuffix=core.windows.net")
        container_name = "ameyocalls"

        response = requests.get(str(recordingFileUrl), stream=True)
        block_blob_service.create_blob_from_stream(container_name, str(sessionId)+'.mp3', response.raw)