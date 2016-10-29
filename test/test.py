import requests
import json

ip = "http://192.168.110.1:8282"


def responseText():
    res = requests.get(ip + '/response/text/1/1')
    status_code = res.status_code
    if (status_code != 200):
        return -1
    else:
        return res.text


def responseBody():
    res = requests.get(ip + '/response/body/1/1')
    status_code = res.status_code
    if (status_code != 200):
        return -1
    else:
        return res.text


def responseJson():
    res = requests.get(ip + '/response/json')
    status_code = res.status_code
    if (status_code != 200):
        return -1
    else:
        return res.text


def redirect():
    res = requests.get(ip + '/response/json')
    status_code = res.status_code
    if (status_code != 200):
        return -1
    else:
        return res.text

texts = responseText()
bodys = responseBody()
jsons = responseJson()
redirects = redirect()

assert texts  == "1"
assert texts != -1
assert bodys  == "Hello, world"
assert bodys != -1
assert jsons == json.dumps({"some": "data"})
assert jsons != -1
assert redirects == json.dumps({"some": "data"})
assert redirects != -1
