import redis
from rq import use_connection

my_connection = redis.StrictRedis(host='localhost', port=6379, db=0, password=None)
#b = '{"processTemplate" : "Financial Statement Template", "perfiosTransactionId" : "ZZZZ12345670123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "Demo", "serialNo" : "DW12023"}'
#my_connection.rpush(1,b)
#b = '{"processTemplate" : "Bank Statement Template", "perfiosTransactionId" : "ZZZZ12345678123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "PRODUCTION", "serialNo" : "DW124"}'
#my_connection.rpush(1,b)
#b = '{"processTemplate" : "ITRV Statement Template", "perfiosTransactionId" : "A123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "Demo", "serialNo" : "DW1250"}'
#my_connection.rpush(1,b)
#b = '{"processingType" : "Financial Statement", "perfiosTransactionId" : "ZAAZ12345670123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "http://192.168.0.38/"}'
#my_connection.rpush(1,b)
#b = '{"processTemplate" : "Financial Statement Template", "perfiosTransactionId" : "ZZZZ1567890123", "downloadUrl" : "https://www.perfios.com/KuberaVault/...", "environment" : "PRODUCTION", "serialNo" : "DW125"}'
b = '{"perfiosTransactionId":"HBAZ1558343585826","processingType":"FINANCIAL_STATEMENT","environment":"https://demo.perfios.com/","startDate":"2018-04-01","endDate":"2019-03-31","organisationName":"kvbSme","downloadUrl":"https://demo.perfios.com/KuberaVault/insights/kvbSme/statements/financial/scanned/process/"}'
my_connection.publish('test_qu', b)



#res = my_connection.llen(1)
#print (res)