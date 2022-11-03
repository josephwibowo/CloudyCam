import logging


logging.basicConfig(level=logging.DEBUG, filemode='w')
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger('CloudyCam')

fileHandler = logging.FileHandler("./logs/cloudycam.log")
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)