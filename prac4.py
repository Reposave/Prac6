import busio
import digitalio
import board
import threading
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from adafruit_debouncer import Debouncer

#Converts the Voltage to a temperature in degrees celcius
def VoltageToTemp(voltage,t_coeff,vzero):
    return (voltage - vzero)/t_coeff
    
#Obtain temp sensor results
def temp_sensor(results):
    chann = AnalogIn(mcp, MCP.P1) #Temp_Sensor
    results[0] = chann.value
    results[1] = chann.voltage

#Obtain LDR results
def ldr_sensor(results):
    chann = AnalogIn(mcp, MCP.P2) #LDR
    results[0] = chann.value

if __name__ == "__main__":
    #temp_sensor
    T_COEFF = 0.01
    VZERO = 0.4
    print_time = 1
    start_time = time.time()
    total_time = 0

    times = [10,5,1]
    times_interval = 0

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    #Setup the button with a 0.1s debounce delay
    button = digitalio.DigitalInOut(board.D23)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    switch = Debouncer(button,interval=0.1)

    # create an analog input channel on pin 2 for LDR

    print(f"{'Runtime' : <10}{'Temp Reading' : <15}{'Temp' : <10}{'Light Reading': <10}")

    while(True):
        switch.update()

        #if the difference between runtime and start time is greater than the print time, execute the body.
        if((time.time()-start_time)>print_time):
            temp_results = [0,0]
            ldr_results = [0,0]

            #Creating new threads.
            temp = threading.Thread(target=temp_sensor,args=(temp_results,))
            
            ldr = threading.Thread(target=ldr_sensor,args=(ldr_results,))  
            ldr.start()
            ldr.join()

            temp.start()
            temp.join()

            total_time+=round(time.time()-start_time)
            print(f"{str(total_time)+'s' : <10}{temp_results[0] : <15}{str(round(VoltageToTemp(temp_results[1],T_COEFF,VZERO), 1)) +'C' : <10}{ldr_results[0] : <10}")
            
            start_time=time.time()
        #checks for button release.
        if(switch.fell):
            
            if(times_interval==2):
                times_interval=0
            else:
                times_interval+=1
            print_time = times[times_interval]
            print("Switched to intervals of: "+ str(print_time))