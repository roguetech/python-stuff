import threading
import time
import logging

def time_keeping(name):
    logging.info("Thread starting %s", name)
    print("inside")
    time.sleep(2)
    print("inside after")
    logging.info("Thread stopped %s", name)

logging.info("starting thread")
x = threading.Thread(target=time_keeping, args=(1,))
print("before")
x.start()
print("after")