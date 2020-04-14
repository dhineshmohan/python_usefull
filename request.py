import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth

headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)', 'Accept' : '*/*', 'Accept-Language': 'en-US', 'Content-Type' : 'application/json;charset=utf-8','Authorization' : 'Bearer UTIGUEST1547639478188', 'Referer' : 'https://www.utimf.com/portal/login'}
hostname = 'http://spoonbill.hinagro.com:8080' #/prohancei/project/config/add'
username = 'sysadmin'
passwrd = 'TGViJHlBSGVpczUyMTcyOTg0MDU2MTEyMTQ3N3BSb0hhTmNFX0RlTGlNaVRlUl9TeU1Cb0xMZWIkeUFIZWlzNTJwUm9IYU5jRV9EZUxpTWlUZVJfU3lNQm9MMTU0NzExNTg4MjczMg=='
sess = requests.Session()
#sess.auth = (username, passwrd)
'''
payload = { 'projectTemplateName' : 'Bank Statement Template',
            'projectTitle' : 'ZSZZB223568',
            'projectCode' : 'BANK-127',
            'projectDescription' : 'perfios.com',
            'type' : 'Bank Statement',
            'category' : 'Bank Statement Processing',
            'startDate' : '2019-01-17',
            'endDate' : '2019-01-17',
            'estimate': '2',
            'manager' : 'govi',
            'assignees' : 'govi',
            'customer' : '',
            'complexity' : '',
            'customAttribute' : '[{Applicant Name:PRODUCTION}]'}
'''
payload = { 'UserId' : 'GYNPK6665L', 'UserPassword' : 'Neha@0002'}
url = 'https://www.utimf.com/account/login/'
#sess.get(url, auth=(username, passwrd))
#print (sess.cookies)
#res = sess.post(url, data=payload)
#print (res.text)

#request.add_header('Authorization', b'Basic ' + base64.b64encode(username + b':' + password))

#hostname = 'http://spoonbill.hinagro.com:8080/prohancei'
#payload = {"projectCode":"BANK-125", "projectTitle":"ZSZZA123568", "startDate":"10 Jan 2019", "endDate":"10 Jan 2019", "estimate":"2", "taskTemplate":"Bank Statement Template","manager":"Narayanan", "assignees": '', "customer": '', "type": "Bank Statement", "category": "Bank Statement Processing", "complexity": "Demo"};

#res = requests.get(url, auth=(username, passwrd))
#print (res)

#response = requests.post(hostname, auth=HTTPBasicAuth(username, passwrd), headers=headers, data=payload, verify=False)
#requests.add_header('Authorization', 'Basic c3lzYWRtaW46VEdWaUpIbEJTR1ZwY3pVeU1UY3lPVGcwTURVMk1URXlNVFEzTjNCU2IwaGhUbU5GWDBSbFRHbE5hVlJsVWw5VGVVMUNiMHhNWldJa2VVRklaV2x6TlRKd1VtOUlZVTVqUlY5RVpVeHBUV2xVWlZKZlUzbE5RbTlNTVRVME56RXhOVGc0TWpjek1nPT0=')
#response = requests.get(url, headers=headers)
#print (response)
response = requests.post(url, headers=headers, data=payload, verify=False)
#response = requests.post(hostname, auth=HTTPBasicAuth('sysadmin', 'Leb$yAHeis52'), headers=headers, data=payload, verify=False)
#response = requests.post(hostname, headers=headers, verify=False)
print (response.text)

#curl https://spoonbill.hinagro.com:8080/prohancei/project/config/add -H "Authorization: sysadmin TGViJHlBSGVpczUyMTcyOTg0MDU2MTEyMTQ3N3BSb0hhTmNFX0RlTGlNaVRlUl9TeU1Cb0xMZWIkeUFIZWlzNTJwUm9IYU5jRV9EZUxpTWlUZVJfU3lNQm9MMTU0NzExNTg4MjczMg==" -H "Content-Type: application/json"
