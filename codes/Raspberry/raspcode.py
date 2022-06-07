import RPi.GPIO as GPIO
import time, json, requests, datetime, serial
import threading, atexit



GPIO.setmode(GPIO.BCM)
#--------------------servo------------------
servo =18
GPIO.setup(servo, GPIO.OUT)
p= GPIO.PWM(servo, 50)  #PMW:펄스 폭 변조


http ="http://59.6.45.112:5000/"
# sens=["lamp","fan1","pump1","heater","pump2","pump3","pump4"]#output-relay
sens=["lamp","pump1","pump2","pump3","pump4","fan1","heater"]#output-relay

sengp=[2,3,4,22,17,10,9]#port
now= datetime.datetime.now()
try:
    ardp = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
except:
    ardp = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)

for pin in sengp: GPIO.setup(pin,GPIO.OUT)#; GPIO.output(s,0)

def stop():
    print("cleanup")
    GPIO.cleanup()

def servo():
    inpt({"food":"2"})
    p.start(0)
    print("2")
    p.ChangeDutyCycle(12.5) #180
    time.sleep(1)
    p.ChangeDutyCycle(2.5)
    time.sleep(1)  
    p.stop
    inpt({"food":"0"})
    print("0")
def inpt(data):#
    htp=''
    hp= ''
    for a,i in enumerate(data):
        if a == 0:
            hp = hp + i + '='+ data[i]
        else:
            hp = hp + '&'+ i + '='+ data[i]
    htp=http+'input?'+hp
    print(htp) 
    try:
        url =requests.get(htp)
    except:
         time.sleep(2)
         url =requests.get(htp)
        
def getjs():
    htp = http+ '/main'
    try:
        url =requests.get(htp)
    except:
        time.sleep(2)
        url =requests.get(htp)
    
    text = url.text
    data = json.loads(text)
    print(data)
    return data
        
# inpt()
# data=getjs()
#only relay control  
def controlSens(data):
    for i in range(len(sens)): 
        if data[sens[i]] =="1":
            GPIO.output(sengp[i],True)
            print(f'{sens[i]} ON')
        elif data[sens[i]] =="0":
            GPIO.output(sengp[i],False)
            #print(f'{sens[i]} is False')
            
def thredMain():
     while True:
        try:
            ins=["temp","ph"]
            now= datetime.datetime.now()
            data=getjs()
            if data["food"] == "1": servo()
            controlSens(data)
            print(now)
            line = ardp.readline().decode('utf-8').rstrip()
            if line:
                In_sens=line.split()
                print(f'1 = {In_sens}')
                dic = { name:value for name, value in zip(ins, In_sens) }         
                print(f'2 = {dic}')                
                time.sleep(0.5)
                inpt(dic)#error
        except:
            continue

t=threading.Thread(target=thredMain)
t.start()

