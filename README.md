
# aiohttp Framework Project 생성

- python에서는 다양한 서버프레임 워크가 존재한다. 그중 하나로 aiohttp에 대해서 다뤄보고자 한다.(해당 문서는 작성자인 멍개님에게 저작권이 있습니다.)
- aiohttp는 가벼우면서 빠르게 짤 수 있다.
- node.js의 express generator처럼 기본 구조를 잡아주는 것을 찾지 못하여 기본 뼈대를 만들었다.


## 서버를 시작하기 앞서 환경셋팅

- aiohttp라는 프레임워크를 사용할거이기 때문에 `aiohttp`라는 모듈을 설치를 해준다.
- 또한 `ayncio` 모듈도 설치를 해준다.
- 로그를 찍기 위해 `logging` 모듈도 설치해준다.
- DB 모듈은 개인 성향에 맞추어서 설치를 해준다.(DB 모듈에 대해서는 문서 아래부분에서 좀더 자세히 설명하겠다.)
(orm을 쓸경우 `sqlalchemy`가 대표적이고 row query를 쓴다면 `pymysql`이나 `MySQLdb`가 대표적이다.)


### 모듈설치 및 python 설정

#### python3.5 설치

```
$ sudo apt-get update ; sudo apt-get upgrade
$ wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz #python3.5.2 다운
$ tar xvf Python-3.5.2.tgz   # 압축풀기
$ cd Python-3.5.2              # 디렉토리 이동
$ ./configure                   # makefile 생성
$ make                         #python코드 컴파일
$ sudo make install            # 설치
```

- 빠른 시일에 virtualenv를 활용하여 파이썬 환경, 모듈의 의존성 문제를 해결하겠다.

#### 모듈설치

- requirements.txt내부에 있는 모듈을 한번에 설치를 해준다.
- 에러가 뜨지 않는다면 정상적으로 설치가 완료 된 것이다.

```.py
pip3 install -r requirements.txt
```

###### requirements.txt 들여다 보기

```
$ cat requirements.txt
aiohttp >= 1.0.5
sqlalchemy >= 1.1.3
mysqlclient >= 1.3.9
aiohttp_jinja2 >= 0.8.0
```

> 파이썬 버전 3.5와 모듈들이 에러없이 설치가 이상없이 완료 됬으면 서버를 실행을해보자. 파이썬은 버전에 따라 비동기 처리 방식이 약간 다르기 떄문에 해당 코드들을 3.5이외의 버전에서 샤용을 할 경우 async 부분에서 에러가 발생 할 수 있다.

### 서버시작

```
python3 app.py
```

해당 소스코드를 그대로 실행을 할 경우 8282포트로 설정이 되어있다. port는 app.py에서 **__init__** 함수내부의 `host`와 `port`를 수정을 위해 configure.conf를 수정해 주면 된다.


### 서버설정

- 설정 파일은 `/configure/conf` 에 작성된다.
- 서버의 기본적인 설정
- 데이터 베이스, 서버 포트 등의 설정정보들

```.py
#데이터 베이스 설정
database = {
        "host":'localhost',
        "password" :'password',
        "user" : 'user',
        "database": 'database'
},


#서버 설정
server = {
    "host" : "0.0.0.0", # 허용 ip 0.0.0.0일 경우 모든 아이피 허용
    "port" : 8282, # 접속 포트
    "message" : "server on 8282 port"  # 서버 시작 메시지
}
```


### app.py의 init함수

```.py
def __init__(loop):

    app = web.Application(loop=loop)

    host = conf.server["host"]
    port = conf.server["port"]

    setup_route(app)
    setup_middlewares(app)

    return app, host, port
```

host를 0.0.0.0으로 하여 모든 IP로부터 접속을 허용을 해준다.


### 라우팅 설정 `routes.py`

- 각 요청에 따른 처리를 만들어 준다.
- `setup_route`를 app에서 호출을 해주면 된다.

```.py
def setup_route(app):
    # get요청
    app.router.add_get('/response/text/{u}/{p}', responseText)
    app.router.add_get('/response/body/{u}/{p}', responseBody)
    app.router.add_get('/response/json', responseJson)
    app.router.add_get('/r', redirect)

    # post요청
    app.router.add_post('/post/test', posttest)

```


### 실제 로직이 처리되는 부분

- 각 요청에 맞추어서 아래처럼 작성을 해주면 된다.
- 각 API마다 등록을 시켜준다.

#### post요청에 대한 처리

---

```.py
@asyncio.coroutine
def posttest(req):
    post_data = yield from req.POST()
    return  web.Response(text= 'test')
```

yield from을 명시하지 않으면 에러가 발생을 한다.
또한 req는 multiDict이라는 방식으로 body를 처리한다. 만약에 list를 서버에게 보낸다면 해당 json.dumps 혹은 JSON.stringify처리를 해서 보낸후 json.loads(yield from req.POST())처리를 하는것이 좋다.


#### get요청에 대한 처리
---

`text`응답
```.py
@asyncio.coroutine
def responseText(req):
    uKey =  req.match_info.get("u") or 'x'
    pKey =  req.match_info.get("p") or 'x'

    size = str(test_module(uKey, pKey))

    return  web.Response(text= size)

```

`body`응답
```.py
@asyncio.coroutine
def responseBody(req):
    return web.Response(body=b"Hello, world")
```

`json`응답
```.py
@asyncio.coroutine
def responseJson(req):
    data = {'some': 'data'}
    return web.json_response(data)
```

`새로고침`
```.py
@asyncio.coroutine
def redirect(req):
    return web.HTTPFound('/response/json')
```

해당 함수는 실제 서버 로직이 실행되는 부분이다. 라우팅에서 설정해준 패스로 접속할 떄 해당 로직을 호출을 한다.

> 개인 성향에 따라서 실제 로직이 처리되는 부분과 라우팅을 나눠도 되고 안나눠도 된다. 또한 API가 늘어날수록 API 종류에 따라서 routes파일을 나누는게 좋다.
node.js에서는 디렉토리를 모듈로 가져오면 해당 디렉토리내의 index.js를 자동으로 가져오는데 python에서는 이점이 조금 다르다.


### 미들웨어 처리

- 미들웨어란 실제 로직부분이 아닌 로직이 처리된기 전, 후의 공통적으로 처리가 된느 부분을 말한다.
- 해당 프레임에서는 404, 500, 200가 됬을때 로그를 남기는 기능만 구현을 하였다.

 ```.py
 #잘못요청
 async def handle_404(request, response):
     user = request.match_info.get("userKey") or 'x'
     product = request.match_info.get("productKey") or 'x'

     error_log(user, product, "404")

     raise web.HTTPNotFound()
 ```

 ```.py
 #서버에러
 async def handle_500(request, response):
     user = request.match_info.get("userKey") or 'x'
     product = request.match_info.get("productKey") or 'x'

     critical_log(user,product,"500")

     return response
 ```

 ```.py
 #성공적으로 처리
 async def handle_200(request, response):
     user = request.match_info.get("userKey") or 'x'
     product = request.match_info.get("productKey") or 'x'
     recommend = response.text or 'x'

     success_log(user, product, recommend)

     return response
 ```

- 각각 응답 코드에 따른 후 처리를 만들었다.
- 이제 이것을 app.middlewares에 등록을 시켜준다.


### 미들웨어등록

```.py
def error_pages(overrides):
    async def middleware(app, handler):
        async def middleware_handler(request):
            try:
                response = await handler(request)
                override = overrides.get(response.status)
                if override is None:
                    return response
                else:
                    return await override(request, response)
            except web.HTTPException as ex:
                override = overrides.get(ex.status)
                if override is None:
                    raise
                else:
                    return await override(request, ex)
        return middleware_handler
    return middleware


def setup_middlewares(app):
    error_middleware = error_pages({404: handle_404,
                                    500: handle_500,
                                    200: handle_200
                                    })
    app.middlewares.append(error_middleware)
```

error_pages에 응답코드를 키값으로 해당 함수를 매핑을 시켜서 인자로 넘겨준다.
app.middlewares에 error_pages의 받환값을 넣어준다.
app파일에서 setup_middlewares에 app인자를 넘겨주어서 호출을 해준다.


### DB 사용

####  - DB를 사용하기 앞서 필요한 모듈 설치

- 해당 프레임워크에서는 sqlalchemy을 사용하여 ORM을 사용할 것이다.
- sqlalchemy는 MySQLdb라는 모듈을 사용하고 있다. mysqlclient도 함께 설치해 준다.
- mysqlclient은 C컴파일이 되어있어 windows에서는 설치가 조금 버거울 수 있다.
- windows에서는 c컴퍼일러가 설치되어 있으면 정상적으로 설치가 될 것이다.
- linux나 mac에서는 아래 명령을 통해 정상적으로 설치가 될 것이다.
- 만약 설치가 되지 않는다면 관리자 권한으로 실행해 주면 된다.

```
pip3 isntall mysqlclient
```

```
pip3 install sqlalchemy
```


#### - db설정

- configure.conf내부의 conf.database를 정의를 해준다.
- configure.database에서 DB 엔진, 세션을 잡아준다.
- database.py에서 정의한 Base를 모델을 정의하는데 사용한다.

```.py

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configure.conf as conf

url = conf.database[0]["category"]+"://"+conf.database[0]["user"]+":"+conf.database[0]["password"]+"@"+conf.database[0]["host"]+"/"+conf.database[0]["database"]

engine = create_engine(url, convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  from models import models

  Base.metadata.create_all(engine)

```

#### - model 정의

- db 세션을 잡았으니 이제 db 모델을 설정을 해준다.
- 모델 정의 클래스는 configure.database에서 정의된 Base로부터 상속을 받는다
- ORM(Object-relational mapping)은 DB 테이블을 객체로 매핑을 해준다.
- ```__tablename__```은 실제 DB에 존재하는 테이블 이름이여야 한다.

```.py
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from configure.database import Base

class Test(Base):
	__tablename__ = 'test'
	id = Column(Integer, primary_key= True, autoincrement=True)
	test = Column(Integer)
	test1 = Column(Integer)
	test2 = Column(String)
	test3 = Column(String)


	def __init__(self, id, test, test1, test2, test3):
		self.id = id
		self.test = test
		self.test1 = test1
		self.test2 = test2
		self.test3 = test3


	def __repr__(self):
		return (self.id, self.test, self.test1, self.test2, self.test3)
```

#### - 정의한 모델, 세션을 import

- 정의한 모델을 사용하여 DB를 쓰기 위해서 아래처럼 import를 해주면 된다.

```.py
from configure.database import init_db
from configure.database import db_session
from models.models import Test
```

> 주로 서버 로직이 실행되는 라우팅 파일쪽에서 많이 사용 될 것이다.

### app.py

- 미들웨어, 라우팅을 app에서 설정을 해준다.
- 해당 모듈들을 불러와서 호출해주기만 해면 된다. web.Application(loop=loop)을 인자로 넘겨준다.

```.py
import asyncio
import logging
from aiohttp import web

from routes import setup_route as setup_route
from middleware import setup_middlewares

import configure.conf as conf

def __init__(loop):

    app = web.Application(loop=loop)

    host = conf.server["host"]
    port = conf.server["port"]

    setup_route(app)
    setup_middlewares(app)

    return app, host, port


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = __init__(loop)

    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    print(conf.server["message"])
    main()
```


### 서버 테스트

- 해당 프레임 워크의 테스트 코드는 `/test/test.py`에서 작성을 하였다.
- 각 요청에 따른 코드를 작성
- 우선 요청을 해주는 requests모듈과 json으로 응답을 받기위해 json모듈을 import 시켜준다.

```.py
import requests
import json

ip = "http://192.168.110.1:8282"
```
서버 ip를 선언을 해주었다.


- text응답 API 요청

```.py
def responseText():
    res = requests.get(ip + '/response/text/1/1')
    status_code = res.status_code
    if (status_code != 200):
        return -1
    else:
        return res.text
```
