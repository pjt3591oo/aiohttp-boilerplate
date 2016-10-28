import requests


def hello():
    return requests.get("localhost:8282/response/text/1/1")


def responseText():
    return True


def responseBody():
    return True


def responseJson():
    return True


def redirect():
    return True
