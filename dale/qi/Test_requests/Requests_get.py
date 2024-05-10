import requests
r = requests.get('https://api.oioweb.cn/api/common/teladress',
                     params={"mobile":"18878976546"})
print(r.status_code)
print(r.json())
print(r.text)