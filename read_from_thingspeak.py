import urllib3,json,conf,re
from datetime import datetime,timedelta

http=urllib3.PoolManager()

url="http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (conf.CHANNEL_ID,conf.READ_KEY)
conn =http.request('GET',url)
response = conn.data.decode('utf8')
data=json.loads(response)
print(data['field1'],data['field2'])
a=list(filter(None,re.split("[-TZ:]+",data['created_at'])))
a.append('1')
b=[]
for i in a: b.append(int(i))
p=datetime(b[0],b[1],b[2],b[3],b[4],b[5],b[6])
p=p+timedelta(seconds=19800)
print("Last update time: "+str(p))
dt=datetime.today()
print("Current fetch time: "+str(dt))
print("Difference in time(in secs): "str((dt-p).seconds))
conn.close()
