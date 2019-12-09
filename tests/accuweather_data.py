import json,urllib3,conf

url='http://dataservice.accuweather.com/currentconditions/v1/%s?apikey=%s&details=true' \
		% (conf.LOCATION_ID_AW, conf.WEATHER_KEY_AW)

http=urllib3.PoolManager()
conn=http.request('GET',url)
response=conn.data.decode('utf8')
data=json.loads(response)
for i in data[0]:
	print(i,end=' ')
	if(isinstance(data[0][i],dict) and 'Imperial' in data[0][i]):
		print(data[0][i]['Imperial']['Value'],end=' ')
		print(data[0][i]['Imperial']['Unit'])
	else:
		print()
		#print(data[0][i])
conn.close()
