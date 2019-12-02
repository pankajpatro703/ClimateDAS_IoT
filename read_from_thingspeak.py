import urllib3,json,conf

http=urllib3.PoolManager()

url="http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (conf.CHANNEL_ID,conf.READ_KEY)

def main():
    conn =http.request('GET',url)
    response = conn.data.decode('utf8')
    data=json.loads(response)
    print(data['field1'])
    print(data['field2'])
    conn.close()

if __name__ == '__main__':
    main()
