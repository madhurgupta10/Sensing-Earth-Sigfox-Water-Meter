#Adapted from https://github.com/SNOC/rpisigfox
import time
import serial
import sys
from time import sleep
import walabot
import json

class Sigfox(object):
    SOH = chr(0x01)
    STX = chr(0x02)
    EOT = chr(0x04)
    ACK = chr(0x06)
    NAK = chr(0x15)
    CAN = chr(0x18)
    CRC = chr(0x43)

    def __init__(self, port):
        # allow serial port choice from parameter - default is /dev/ttyAMA0
        portName = port
        
        print('Serial port : ' + portName)
        self.ser = serial.Serial(
                port=portName,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
        )

    def getc(self, size, timeout=1):
        return ser.read(size)

    def putc(self, data, timeout=1):
        ser.write(data)
        sleep(0.001) # give device time to prepare new buffer and start sending it

    def WaitFor(self, success, failure, timeOut):
        return self.ReceiveUntil(success, failure, timeOut) != ''

    def ReceiveUntil(self, success, failure, timeOut):
            iterCount = timeOut / 0.1
            self.ser.timeout = 0.1
            currentMsg = ''
            while iterCount >= 0 and success not in currentMsg and failure not in currentMsg :
                    sleep(0.1)
                    while self.ser.inWaiting() > 0 : # bunch of data ready for reading
                            c = self.ser.read()
                            currentMsg += c
                    iterCount -= 1
            if success in currentMsg :
                    return currentMsg
            elif failure in currentMsg :
                    print('Failure (' + currentMsg.replace('\r\n', '') + ')')
            else :
                    print('Receive timeout (' + currentMsg.replace('\r\n', '') + ')')
            return ''

    def sendMessage(self, message):
        print('Sending SigFox Message...')
        
        if(self.ser.isOpen() == True): # on some platforms the serial port needs to be closed first 
            self.ser.close()

        try:
            self.ser.open()
        except serial.SerialException as e:
            sys.stderr.write("Could not open serial port {}: {}\n".format(ser.name, e))
            sys.exit(1)

        self.ser.write('AT\r')
        if self.WaitFor('OK', 'ERROR', 3) :
                print('SigFox Modem OK')

                self.ser.write("AT$SS={0}\r".format(message))
                print('Sending ...')
                if self.WaitFor('OK', 'ERROR', 15) :
                        print('OK Message sent')

        else:
                print('SigFox Modem Error')

        self.ser.close()

if __name__ == '__main__':
    
    def split_by_length(s,block_size):
    w=[]
    n=len(s)
    for i in range(0,n,block_size):
        w.append(s[i:i+block_size])
    return w
    
    if len(sys.argv) == 3:
            portName = sys.argv[2]
            sgfx = Sigfox(portName)
    else:
        sgfx = Sigfox('/dev/ttyAMA0')
    arduino = serial.Serial('/dev/ttyACM0', 9600)

    while True:
        data = arduino.readline()   #read data from arduino
        if data:
            message = json.loads(data[0])
            message['count'] = PeopleCounterApp()

    message = json.dumps(message, ensure_ascii=False)
    message = message.encode().hex()
    message_list = split_by_length(message, 24)
    if len(sys.argv) > 1:
        message = "{0}".format(sys.argv[1])
    for m in message_list:
        sgfx.sendMessage(m)
    time.sleep(600) #sleep for 10 min
