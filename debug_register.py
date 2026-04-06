import json
import urllib.request
import urllib.error

url = 'http://127.0.0.1:5000/api/auth/register/patient'
data = {
    'firstName': 'test1',
    'lastName': 'test',
    'age': '20',
    'location': 'mumbai, india',
    'email': 'test1@gmail.com',
    'password': 'testpass'
}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    resp = urllib.request.urlopen(req)
    print(resp.status)
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP', e.code)
    print(e.read().decode())
except Exception as e:
    print('ERR', e)
