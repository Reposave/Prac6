import busio
import digitalio
import board
import threading
import time
import socket
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from adafruit_debouncer import Debouncer
from datetime import datetime

MESSAGE = ""

def TcpListener(results):
    while(True):
        data = s.recv(BUFFER_SIZE).decode()
        results[0] = data

        if(data == "x"):
            sendoff(results) #Turn Off
        elif(data == "o"):
            sendon(results) #Turn On
        elif(data == "c"):
            check() #Status

        time.sleep(sleep)

def sendon(results):
    results[3] = "o"
    
def sendoff(results):
    results[3] = "x"

def check():
    lock.acquire()
    TOSEND = 'c ' + temp_results[3] + ' ' + str(len(MESSAGE.encode('utf-8'))) + ' ' + MESSAGE
    s.send(TOSEND.encode())
    lock.release()
    
lock = threading.Lock()

#Converts the Voltage to a temperature in degrees celcius
def VoltageToTemp(voltage,t_coeff,vzero):
    return (voltage - vzero)/t_coeff
    
#Obtain temp sensor results
def temp_sensor(results):
    chann = AnalogIn(mcp, MCP.P1) #Temp_Sensor
    results[0] = chann.value
    results[1] = round(VoltageToTemp(chann.voltage,T_COEFF,VZERO), 1)

#Obtain LDR results
def ldr_sensor(results):
    chann = AnalogIn(mcp, MCP.P2) #LDR
    results[0] = chann.value

if __name__ == "__main__":
    
    sleep = 2

    print("Hello")

    TCP_IP = '192.168.43.209'
    TCP_PORT = 5003
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    print("Client connected to Server!")

    temp_results = [0,0,0,'o']

    print("Starting thread...")
    tcpListen = threading.Thread(target=TcpListener,args=(temp_results,))

    tcpListen.daemon = True
    #inputlistener.daemon = True

    #inputlistener.start()
    tcpListen.start()

    #temp_sensor
    T_COEFF = 0.01
    VZERO = 0.4
    print_time = 10
    start_time = time.time()
    total_time = 0

    times = [10,5,1]
    times_interval = 0
    
    press_time = 0

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    #Setup the button with a 0.1s debounce delay-----------------
    button = digitalio.DigitalInOut(board.D23)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    switch = Debouncer(button,interval=0.1)

    print(f"{'Runtime' : <10}{'Temp Reading' : <15}{'Temp' : <10}{'Light Reading': <10}")

    while(True):
        switch.update()

        #if the difference between runtime and start time is greater than the print time, execute the body.
        if((time.time()-start_time)>print_time):
            ldr_results = [0,0]

            if(temp_results[3] == "o"):
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
            
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")

                lock.acquire() #Using locks here to make sure the message isn't altered by other functions
                MESSAGE = current_time + ', ' + str(temp_results[0]) +', ' + str(temp_results[1]) +'C, ' + str(ldr_results[0])
                TOSEND = 's ' + str(len(MESSAGE.encode('utf-8'))) + ' ' + MESSAGE
                s.send(TOSEND.encode())
                lock.release()
                print(TOSEND)
            
            time.sleep(sleep)

        #checks for button release.-------------------------------
        if(switch.rose):
            if((time.time()-press_time)>5):
                print("Goodbye")
                break

        #checks for button press.---------------------
        if(switch.fell):
            s.close() #close socket.

            press_time = time.time()

            if(times_interval==2):
                times_interval=0
            else:
                times_interval+=1
            print_time = times[times_interval]
            print("Switched to intervals of: "+ str(print_time))