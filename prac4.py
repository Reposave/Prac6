import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#temp_sensor
T_COEFF = 100
OFFSET = 0.5
print_time = 10
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

button = digitalio.DigitalInOut(board.D23)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# create an analog input channel on pin 2 for LDR
chan = AnalogIn(mcp, MCP.P2) #LDR
chan2 = AnalogIn(mcp, MCP.P1) #Temp_Sensor

print(f"{'Runtime' : <10}{'Temp Reading' : <15}{'Temp' : <10}{'Light Reading': <10}")

while(True):

    if((time.time()-start_time)>print_time):   
        print(f"{str(total_time)+'s' : <10}{chan2.value : <15}{str(round(chan2.voltage, 4))+'C' : <10}{chan.value : <10}")
        total_time+=print_time
        start_time=time.time()

    if(button.value==0):

        if(times_interval==2):
            times_interval=0
        else:
            times_interval+=1
        
        print_time = times[times_interval]

def VoltageToTemp(voltage,t_coeff,offset):
    return ((voltage - offset)*t_coeff)
    
#def Temp(chann):
    #results = [chann.value, chann.voltage]
    #return results