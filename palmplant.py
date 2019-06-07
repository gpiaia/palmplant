import numpy as np
from scipy.integrate import odeint
import paho.mqtt.client as mqtt
import time
import socket
import serial

def create_file_model():
    f= open("Model.py","w")

    global model_str
    model_str = model_str.replace(" ", "")
    split_str = model_str.split('$')
    parameters = split_str[0].split(',')
    variables = split_str[1].split(',')
    dydts = split_str[2].split(',')

    tab = '    '
    parameters_str = ''
    
    for x in range(0,len(parameters)):
        parameters_str += tab + tab + parameters[x] + '\n'

    variables_str = tab + tab
    var_values = []
    initial_values = []

    for x in range(0,len(variables)):
        var_values.append(variables[x].split('='))

        if(var_values[x][0] != "t"):
            variables_str += var_values[x][0]
            if(x!=len(variables)-2):
                variables_str += ','
            initial_values.append(var_values[x][1])
    variables_str += ' = y\n'      

    dydts_str = tab + tab + "derivs = [";

    for x in range(0,len(dydts)):
        if(x!=0):
            dydts_str += tab + tab + tab + tab  + ' '
        dydts_str += dydts[x] 
        
        if(x!=len(dydts)-1):
            dydts_str +=  ',\n'
        else:
            dydts_str +=  ']\n'
        
    user_model = parameters_str + variables_str + dydts_str
    
    model = ("import numpy as np \r\n" +
             "class model:\r"
             "    def __init__(self):\r" +
             "        print('Init model')\n" +
             "    def function(y, t): \n") + user_model
    
    model += "        return derivs"
    
    f.write(model)
    return  initial_values


def solver():
    # Initial values
    theta0 = 0.0     # initial angular displacement
    omega0 = 0.0     # initial angular velocity
    
    # Bundle initial conditions for ODE solver
    
    print ('Creating model... ')
    y0 = create_file_model()
    y0 = [theta0, omega0]
    # Make time array for solution
    tStop = 2000.
    tInc = 0.05
    t = np.arange(0., tStop, tInc)
    
    cnt = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')

    s.connect((HOST, PORT))

    print ('Importing the model ...')
    from Model import model
    
    print ('Opening the serial port ...')
    ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

    print('Solving ...')
    time_init = time.time()
    for x in range(len(t)-1):
        y = odeint(model.function, y0, [t[x], t[x+1]])
        y0 = y[1]
        y_b=ser.read(4)
        
        ser.write(y_b)

        cnt = cnt + 1
        if(cnt >= 10):
            s.send(y[0,0]) 
            cnt = 0;

    print(time.time()-time_init)
    s.close()
    ser.close()
    print ('Socket and Serial closed')
    
def on_message(client, userdata, message):
    global model_str 
    model_str = str(message.payload.decode("utf-8"))
    solver()
    print('Solution complete')

broker_address="localhost"
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
client.subscribe("modelo/#")

# Configs for tcp socket
HOST = 'localhost' # Symbolic name, meaning all available interfaces
PORT = 8888 #Arbitrary non-privileged port
model_str = ""

print("Running")

while True:
    time.sleep(1)