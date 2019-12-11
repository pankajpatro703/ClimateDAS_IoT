import requests,json,conf

base_url="http://api.openweathermap.org/data/2.5/forecast?"
#complete_url = base_url + "appid=" + conf.WEATHER_KEY_OW + "&q=" + conf.CITY_NAME
complete_url = base_url + "appid=" + conf.WEATHER_KEY_OW + "&id=" + conf.LOCATION_ID_OW
response=requests.get(complete_url)
x=response.json()
data=x['list'][1]
for i in data:
	print(i,end=' ')
	print(data[i])
response.close()

