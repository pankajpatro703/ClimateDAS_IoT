from boltiot import Bolt
from datetime import datetime
import conf,time
import urllib3,json,requests

mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
http=urllib3.PoolManager()

def fetch_data(channel_id,read_key):
	"""Returns data-temperature and light intensity from Thingspeak channel"""
	try:
		url="http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
			 % (channel_id,read_key)
		conn=http.request('GET',url)
		response=conn.data.decode('utf8')
		data=json.loads(response)
		conn.close()
		return(int(data['field1']),int(data['field2']))
	except Exception as e:
		print("Could not fetch data from Thingspeak")
		print(e)
		return(-999,-999)

def fetch_openweather(city_name):
	"""Returns data from openweather"""
	try:
		base_url="http://api.openweathermap.org/data/2.5/weather?"
		complete_url = base_url + "appid=" + conf.WEATHER_KEY_OW + "&q=" + city_name
		response=requests.get(complete_url)
		data=response.json()
		temp_min=data['main']['temp_min']-273.15
		temp_max=data['main']['temp_max']-273.15
		response.close()
		return(temp_max,temp_min)
	except Exception as e:
		print("Could not fetch data from Openweather")
		print(e)
		return(-999,-999)

def fetch_accuweather(location_id,api_key):
	"""Returns data from accuweather"""
	try:
		url='http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/%s?apikey=%s&details=true' \
			% (location_id,api_key)
		conn=http.request('GET',url)
		response=conn.data.decode('utf8')
		data=json.loads(response)
		conn.close()
		return(int(data[0]['RainProbability']))
	except Exception as e:
		print("Could not fetch data from Accuweather")
		print(e)
		return(-999)
	
def post_data(content,write_key):
	"""Sends data to Thingspeak"""
	try:
		url='http://api.thingspeak.com/update'
		key={'api_key':write_key}
		payload=dict(key,**content)
		resp=requests.post(url,params=payload)
		resp.close()
	except Exception as e:
		print("Could not write data to Thingspeak")
		print(e)

def write_to_bolt(data):
	"""Sends the data to BoltIoT module to transmit it over serial"""
	try:
		resp=mybolt.serialBegin(9600)
		data=json.loads(resp)
		if(data['success']==0):
			print('Could not communicate with Bolt')
		else:
			mybolt.serialWrite(str(data['field1'])+" "+str(data['field2'])+" "+str(data['field3'])+" "+str(data['command'])+" \n")
	except Exception as e:
		print("Could not write data to Bolt")
		print(e)
	
def main():
	"""Main function"""
	dt=datetime.today()
	waits=120
	data3,data4=0,0
	while(True):
		data={}
		time.sleep(30)
		waits+=1							#30 secs
		data['field1'],data['field2']=fetch_data(conf.CHANNEL_ID,conf.READ_KEY)	#get sensor data from thingspeak
		if(waits>=120):						#120*30 secs=1 hour, update every 1 hour
			if(dt.month>2 and dt.month<7):		#summer
				data3=fetch_openweather(conf.CITY_NAME)[0]	#get maximum temperature
				data4=0				
			elif(dt.month>6 and dt.month<11):	#monsoon
				data3=fetch_accuweather(conf.LOCATION_ID_AW, conf.WEATHER_KEY_AW)	#get chances of precipitation
				data4=1			
			else:								#winter
				data3=fetch_openweather(conf.CITY_NAME)[1]	#get minimum temperature
				data4=2
			waits=0
		data['field3']=data3
		data['command']=data4	
		for i in data:
			if(data[i]==-999):
				continue					#if any errors, start again
		write_to_bolt(data)					#send data to be displayed on LCD
		print(data)
		del(data['command'])				#delete command before posting
		time.sleep(30)
		waits+=1							#30 secs
		post_data(data,conf.WRITE_KEY)		#post 3rd data to thingspeak

if(__name__=='__main__'):
	main()
