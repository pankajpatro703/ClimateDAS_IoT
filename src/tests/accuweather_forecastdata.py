import json,urllib3,conf

url='http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/%s?apikey=%s&details=true' \
		% (conf.LOCATION_ID_AW, conf.WEATHER_KEY_AW)

http=urllib3.PoolManager()
conn=http.request('GET',url)
response=conn.data.decode('utf8')
data=json.loads(response)
for i in data[0]:
	print(i,end=' ')
	print(data[0][i])
conn.close()

