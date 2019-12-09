import requests,json,conf

base_url="http://api.openweathermap.org/data/2.5/weather?"
#complete_url = base_url + "appid=" + conf.WEATHER_KEY_OW + "&q=" + conf.CITY_NAME
complete_url = base_url + "appid=" + conf.WEATHER_KEY_OW + "&id=" + conf.LOCATION_ID_OW
response=requests.get(complete_url)
x=response.json()
for i in x:
	print(i,end=' ')
	print(x[i])
response.close()

