import redis
import json
POOL = redis.ConnectionPool(host='redisengineering.redis.cache.windows.net', port=6379,password='QrtfUtgtqvZ5JmQlySiqJc3PkyHttrufqAzCaMMPbNg=')
redisCon = redis.StrictRedis(connection_pool=POOL, charset="utf-8", decode_responses=True)
import requests
# r.incr('testingportCounter', 500)
# redisCon.set('63636272af534521da1370ae', json.dumps({"reattempt":4,"disposition":{"failed":30,"busy":30,"no answer":30,"customer hangup":30,"greet":30,"payment info conveyed":30,"refuse to pay":30,"request to call":30}}))
# redisCon.set('636361e95d16c9225df9aa70', json.dumps({"reattempt":4,"disposition":{"failed":30,"busy":30,"no answer":30,"customer hangup":30,"greet":30,"payment info conveyed":30,"refuse to pay":30,"request to call":30}}))
# redisCon.set('636361411908cb223986bf79', json.dumps({"reattempt":4,"disposition":{"failed":30,"busy":30,"no answer":30,"customer hangup":30,"greet":30,"payment info conveyed":30,"refuse to pay":30,"request to call":30}}))
# print(redisCon.get('2d273ae42a5576c1e47067400a3a16bm'))
# data = json.loads(redisCon.get('636ce123ef743b70c0d6ea48')) 
# data["disposition"]["general - right party contact"] = "2"
# print("Data :", data)
# redisCon.set("636ce123ef743b70c0d6ea48",json.dumps(data))
print(redisCon.get('67f86f701a35565a55c75be9618f16bn'))
print(redisCon.get('637cea536184c924db175382'))
print(redisCon.get('5d0506ca900d3529ce84701a305a16bn'))
print(redisCon.get('637ceab263a1b2774087001f'))
print(redisCon.get('a2796286f50039cb2b7b17bcf49d16bn'))

postCallData = {'Sid': 'a2ab269b717052ecd287aab7de7516aa', 'ParentCallSid': None, 'DateCreated': '2022-10-10 09:31:08', 'DateUpdated': '2022-10-10 09:31:26', 'AccountSid': 'saarthi3', 'To': '07314851866', 'From': '08884974479', 'PhoneNumberSid': '53ceecdfaeff96fb37b0f7f3879962e0', 'Status': 'completed', 'StartTime': '2022-10-10 09:31:22', 'EndTime': '2022-10-10 09:31:26', 'Duration': None, 'Price': None, 'Direction': 'outbound-api', 'AnsweredBy': None, 'ForwardedFrom': None, 'CallerName': None, 'Uri': '/v1/Accounts/saarthi3/Calls/a2ab269b717052ecd287aab7de7516aa', 'RecordingUrl': None, 'Details': {'ConversationDuration': None, 'Leg1Status': 'completed', 'Leg2Status': None, 'Legs': {'Leg': {'Id': '1', 'OnCallDuration': '5'}}}}
try:
    if postCallData['Details']['ConversationDuration'] == None:
        try:
            talkTime =  postCallData['Details']['Legs']['Leg']['OnCallDuration']
        except:
            talkTime =  postCallData['Details']['Legs']['Leg'][-1]['OnCallDuration']

    else:
        talkTime =  postCallData['Details']['ConversationDuration']
except:
    pass
    
print("talkTime :",talkTime)
# print("151d6579d338a5518be7929ed62316a9 :",r.get('151d6579d338a5518be7929ed62316a9'))
# print("b16f94ab827f6b2f4c6e500d0cdb16a9 :",r.get('b16f94ab827f6b2f4c6e500d0cdb16a9'))
# print("151d6579d338a5518be7929ed62316a9 :",r.get('151d6579d338a5518be7929ed62316a9'))
# print("151d6579d338a5518be7929ed62316a9 :",r.get('151d6579d338a5518be7929ed62316a9'))
# print("151d6579d338a5518be7929ed62316a9 :",r.get('151d6579d338a5518be7929ed62316a9'))
# print("151d6579d338a5518be7929ed62316a9 :",r.get('151d6579d338a5518be7929ed62316a9'))
# print("151d6579d338a5518be7929ed62316a9 :",r.get('151d6579d338a5518be7929ed62316a9'))
# testingportCounter = r.get('testingportCounter')
# print(r.get('testingPreviousPorts'))
# r.incr('1234-portCounter', 1000)
# r.incr('12345-portCounter', 1000)
# campaignData = json.loads(r.get('6342ef5cb4daff2d1b067a9c'))
# print("campaignData :",campaignData)
# data = {
#     'disposition':'Failed'
# }
# {'reattempt': 4, 'disposition': {'Failed': 120, 'Busy': 121, 'No-Answer': 121, 'Customer Hangup': 120}}
# r.delete('6342ef5cb4daff2d1b067a9c-portCounter')
# r.delete('6342ef5cb4daff2d1b067a9c-previousPorts')
# r.delete('6342f010789ddc133939b60a')
# r.delete('6342f010789ddc133939b60d')
# r.delete('6342f010789ddc133939b60f')
# dispositonData = campaignData.get('disposition')
# mintues = dispositonData.get(data['disposition'])
# print("mintues :", mintues)
# print("campaignData :",campaignData)
# print("testingportCounter :",json.loads(testingportCounter))


# 12345-portCounter = 500
# 12345-previous = None
# return 500
# set 12345-previous = 500

# 12345-portCounter = 1000
# 12345-previous = 500
# return 1000-500

def publishMessageBucket(data):
    print("publishMessageBucket :",data)
    try:
        campaignData = json.loads(redisCon.get(data['campaignId']))
        print("campaignData :",campaignData)
        if campaignData.get('disposition')!= None:
            dispositonData = campaignData.get('disposition')
            print("dispositonData :",dispositonData)
            mintues = dispositonData.get(data['disposition'])
            maximumAttempt = campaignData['reattempt']
            print("maximumAttempt :",maximumAttempt)
            callingIdCount =  json.loads(redisCon.get(data['callingId']))
            print("callingIdCount :",callingIdCount)
            if int(maximumAttempt != None):
                if int(callingIdCount)+1 >= maximumAttempt:
                    pass
                else:
                    url = "https://bucketization.saarthi.ai/bucketlizationFastApi/bucketization/distribution"
                    newData = {
                        "data":data,
                        "minutes":mintues
                    }
                    payload = json.dumps(newData)
                    print("publishMessageBucket payload :",payload)
                    headers = {
                    'Content-Type': 'application/json'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    # print(response.text)
        else:
            pass
    except Exception as e:
        pass
        print("publishMessageBucket exception :", e)

# newdata = {'connectionStatus': 'Not Connected', 'sessionId': '00176304a936fbc3a9660f3b237b16aa', 'disposition': 'no-answer', 'mobile': '08884974479', 'callingId': '6343804d9eee7512a1459b00', 'campaignId': '63437f9ccad8bc30485b9a3e'}
# publishMessageBucket(newdata)