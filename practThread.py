import threading
import queue

def getVelocity(q1):
	#rlock.acquire()
	velocity = q1.get()
	velocity += 1.0
	q1.put(velocity)
	#rlock.release()

def sendVel(q1):
	#rlock.acquire()
	print(q1.get())
	#rlock.release()

def main():
	q1 = queue.Queue()
	print(q1.qsize())
	loopNum = 0
	velocity = 0.0
	q1.put(velocity)
	while (loopNum < 6):
		t1 = threading.Thread(target=getVelocity, args=(q1,))
		t2 = threading.Thread(target=sendVel, args=(q1,))
		t1.start()
		t1.join()
		print(q1.qsize())
		t2.start()
		t2.join()
		print(q1.qsize())
		loopNum += 1

main()
