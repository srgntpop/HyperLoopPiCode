import _thread
import time

value = 10

# TODO:
# - understand how to terminate a thread at will
# - understand how to run a thread for a given duration
# - understand how to pass values btwn threads

def derp_A(valueIn):
	start_time = time.time()
	current_time = time.time()
	while (current_time - start_time < 5.0):
		valueIn+=1
		current_time = time.time()
	
def derp_B(valueIn):
	while 1:
		print("valueIn: " + str(value))

def main():
	print("entering main function")
	try:
		_thread.start_new_thread(derp_A, (value,))
		_thread.start_new_thread(derp_B, (value,))
		#print("threading success")
		time.sleep(100)
	except Exception as exc:
		print("threading failed")
		print(exc)
	#_thread.exit()
main()
