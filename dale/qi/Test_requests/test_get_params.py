import requests

def test_mobile():
    r = requests.get('https://api.oioweb.cn/api/common/teladress',
                     params={"mobile":"18878976546"})
    print(r.status_code)
    assert r.status_code == 200
    result=r.json()
    assert result['msg']=='success'
    assert result['result']['areaCode']=='0771'
    assert result['result']['provCode'] == '450000'
    assert result['result']['cityCode'] == '450100'
    assert result['result']['num'] == 1887897
    assert result['result']['type'] == 1
    assert result['result']['prov'] == '广西'


