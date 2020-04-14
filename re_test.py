import redis
import datetime
import time
from rq import use_connection
import re

my_connection = redis.StrictRedis(host='localhost', port=6379, db=0, password=None)
#b = '{"processTemplate" : "Financial Statement Template", "perfiosTransactionId" : "ZZZZ12345670123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "Demo", "serialNo" : "DW12023"}'
#my_connection.rpush(1,b)
#b = '{"processTemplate" : "Bank Statement Template", "perfiosTransactionId" : "ZZZZ12345678123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "PRODUCTION", "serialNo" : "DW124"}'
#my_connection.rpush(1,b)
b = '{"processTemplate" : "ITRV Statement Template", "perfiosTransactionId" : "ZZZZ1567890123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "Demo", "serialNo" : "DW1250"}'
#my_connection.rpush(1,b)
#b = '{"processTemplate" : "Bank Statement Template", "perfiosTransactionId" : "ZZZZ1567890123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "PRODUCTION", "serialNo" : "DW125"}'
#my_connection.rpush(1,b)
#b = '{"processTemplate" : "Financial Statement Template", "perfiosTransactionId" : "ZZZZ1567890123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "PRODUCTION", "serialNo" : "DW125"}'
print (my_connection.lpop('test_qu'))
tim = datetime.datetime.now()
tim = str(tim)[11:]
print (tim)
li = []
li = tim.split(':')
if int(li[0]) >= 20:
	if re.search(r'^0(.*?)$', li[1]):
		li[1] = li[1][1:]
	else:
		li[1] = li[1]
	print (li[1])
else:
	print ("Less than 20 Hrs")

#print (b)
expected_json = '{"processTemplate" : "Financial Statement Template", "perfiosTransactionId" : "ZZZZ1234567890123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "PRODUCTION", "serialNo" : "DW123"}'

#res = my_connection.llen(1)
#print (res)