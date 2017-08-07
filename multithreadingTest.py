import threading, time
import queue as queue

rLock = threading.RLock()

def readVn100(velocity, q):
	print("acquiring rLock in readVn100")
	rLock.acquire()
	print("rLock acquired")

	try:
		velocity += 2
		q.put(velocity)
		print("sending data")
	finally:
		print("releasign lock vn100")
		rLock.release()
		print("rLock released vn100")

def networkConnect(velocity, q):
	print("acquiring rLock in ntwrkConnect")
	rLock.acquire()
	print("rLock acquired")
	try:
		velocity = q.get()
		print("velocity received: " + str(velocity))
	finally:
		print("releasign lock ntwrkConn")
		rLock.release()
		print("rLock released ntwrkConn")

def vnThread(velocity, q):
	while 1:
		print("enter vnThread")
		readVn100(velocity, q)

def networkThread(velocity, q):
	while 1:
		print("enter ntwrkThread")
		networkConnect(velocity, q)

def startThreads():
	q = queue.Queue()
	velocity = 20.0
	q.put(velocity)
	
	try: 
		
		thread2 = threading.Thread(target=readVn100, name="vn100Thread", args=(velocity, q, ))
		thread2.start()

		thread1 = threading.Thread(target=networkThread, name="networkThread", args=(velocity, q, ))
		thread1.start()
		
		thread2.join()
		thread1.join()

	except Exception as excStr:
		print("problem with threads: ")
		print(excStr)


def main():
	startThreads()

main()
