import logging
import threading

logging.basicConfig(level=logging.DEBUG,
format='(%(threadName)-10s) %(message)s',
)

def worker1(): 
    logging.debug('Starting...')
    counter = 1
    while True:
        if threading.active_count() <= 1: 
            logging.debug('Counter: %d', counter) 
            if counter == 5:
                logging.debug('Counter is now at 5. Starting worker2() thread...') 
                t2.start()
                e2.set()
            counter += 1
        if threading.active_count() > 1: 
            e1.wait()
            if threading.active_count() == 1:
                break
            e1.clear()
            logging.debug('Counter: %d', counter) 
            counter += 1
            e2.set()
    logging.debug('Terminating...')

def worker2():
    alphabet = 65
    for i in range(26):
        e2.wait()
        e2.clear()
        logging.debug('Alphabet: %s',  chr(alphabet))
        if alphabet == 76:
            t3.start() 
            logging.debug('Alphabet is now at L. Starting worker3() thread...') 
        alphabet += 1
        if not t3.is_alive():
            e1.set()
        else:
            e3.set()
        if alphabet == 91:
            break

def worker3():
    reversecounter = 15
    for i in range(15): 
        e3.wait()
        e3.clear()
        logging.debug('ReverseCounter: %d', reversecounter) 
        reversecounter -= 1
        e1.set()
        if reversecounter == 0:
            break

e1 = threading.Event()
e2 = threading.Event()
e3 = threading.Event()
t2 = threading.Thread(target=worker2)
t3 = threading.Thread(target=worker3)

worker1()