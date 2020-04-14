import redis
import datetime
import time
import re


while (True) :
	tim = datetime.datetime.now()
	print (str(tim)[:10])
	tim = str(tim)[11:]
	print (tim)
	li = []
	li = tim.split(':')
	if int(li[0]) >= 9:
		if re.search(r'^0(.*?)$', li[1]):
			li[1] = li[1][1:]
		else:
			li[1] = li[1]
		if int(li[1]) >= 9:
			print (li[1])
			print ("Time to quit")
			break
	else:
		print ("Hello")