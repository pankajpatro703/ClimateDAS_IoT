import requests,conf

def post(key,content):
	URL='http://api.thingspeak.com/update'
	key={'api_key':key}
	payload=dict(key,**content)
	resp=requests.post(URL,params=payload)
	print(resp.status_code)
	print(int(resp.content))
data={}
data['field1']=96	#
data['field2']=21	#
#chances=3
#data['field3']=chances
post(conf.WRITE_KEY,data)

