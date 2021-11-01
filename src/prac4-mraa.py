import threading
import time
from mraa import *

def printstuff():
    print("lol")

if __name__ == "__main__":
    #temp_sensor
    T_COEFF = 0.01
    VZERO = 0.4
    print_time = 1
    start_time = time.time()
    total_time = 0

    times = [10,5,1]
    times_interval = 0
    
    press_time = 0

    #Setup the button with a 0.1s debounce delay-----------------
    button = Gpio(23)
    button.dir(DIR_IN)
    button.isr(EDGE_BOTH, printstuff)

    print(f"{'Runtime' : <10}{'Temp Reading' : <15}{'Temp' : <10}{'Light Reading': <10}")

    while(True):

        #if the difference between runtime and start time is greater than the print time, execute the body.
        if((time.time()-start_time)>print_time):
            temp_results = [0,0]
            ldr_results = [0,0]

            #Creating new threads.
            temp = threading.Thread(target=temp_sensor,args=(temp_results,))
            temp.daemon = True
            
            ldr = threading.Thread(target=ldr_sensor,args=(ldr_results,)) 

            ldr.start()
            temp.start()
            ldr.join()
            temp.join()

            total_time+=round(time.time()-start_time)
            print(f"{str(total_time)+'s' : <10}{temp_results[0] : <15}{str(temp_results[1]) +'C' : <10}{ldr_results[0] : <10}")
            
            start_time=time.time()
        