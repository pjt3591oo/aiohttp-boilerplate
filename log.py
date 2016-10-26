import logging
import asyncio

logger = logging.getLogger('log')
fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
fileHandler = logging.FileHandler('./log/log.log')
streamHandler = logging.StreamHandler()
fileHandler.setFormatter(fomatter)
streamHandler.setFormatter(fomatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)


# @asyncio.coroutine
#정상적으로 추천이 완료 된 경우
def success_log(user, product, recommend):
    print('log success')
    msg = 'code : 200, user : '+ str(user) + ', product : '+ str(product) + ', recommend : '+ str(recommend)
    logger.info(msg)
    print('log success 1')


@asyncio.coroutine
#서버에러가 떴을 경우
def critical_log(user, product):
    msg = 'code : 500, user : '+ user + ', product : '+ product
    logger.critical(msg)

@asyncio.coroutine
def error_log(user, product):
    msg = 'code : 500, user : '+ user + ', product : '+ product
    logger.error(msg)





# def log_write(user, product, recommend):
