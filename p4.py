import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

btn_submit = 16
button = 0
printval = False
#To Do
#look at threading.
#draw a circuit diagram.
#draw a flow chart.

def menu():
    # create an analog input channel on pin 3
    chan = AnalogIn(mcp, MCP.P1)

    print("Temp Sensor.")
    print("Raw ADC Value: ", chan.value)
    print("ADC Voltage: " + str(chan.voltage) + "V")

    # create an analog input channel on pin 3
    chan = AnalogIn(mcp, MCP.P2)

    print("LDR")
    print("Raw ADC Value: ", chan.value)
    print("ADC Voltage: " + str(chan.voltage) + "V")

def setup():
    global button
    # Setup board mode
    # Setup regular GPIO
    # Setup PWM channels
    # Setup debouncing and callbacks

    button = digitalio.DigitalInOut(board.D23)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    print("Success")
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    pass

# Guess button
def btn_guess_pressed(channel):
    print("Hello")
    pass

if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        
        while True:
            if(button.value == 0):
                menu()
            pass
    except Exception as e:
        print(e)
    finally:
        