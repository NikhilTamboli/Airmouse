import socket
import struct
import errno
import pyautogui
import math

g=9.2

# General config
UDP_IP = "192.168.0.203"  # Change to your ip
UDP_PORT = 8888
MESSAGE_LENGTH = 13  # one sensor data frame has 13 bytes

# Prepare UDP
print("This PC's IP: ", UDP_IP)
print("Listening on Port: ", UDP_PORT)
sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind((UDP_IP, UDP_PORT))

xraw,yraw,zraw,tilt,vel,roll=0,0,0,0,0,0
xprev,yprev,zprev=0,0,0

sensx,sensy,sensz=0.05,0.05,0.0

def getMovement(disp,sens):
    if abs(disp)>sens:
        return round(disp,2)
    else:
        return 0

# Read data forever
while True:
    # Get latest data
    keepReceiving = True
    newestData = None
    newestData2 = None
    while keepReceiving:
        try:
            data, fromAddr = sock.recvfrom(MESSAGE_LENGTH)
            if data:
                newestData = data
                id = data[0]
        except socket.error as why:
            if why.args[0] == errno.EWOULDBLOCK:
                keepReceiving = False
            else:
                raise why

    if newestData is not None:
        # print(id)
        if(id==1):
            xac = eval("%1.6f" % struct.unpack_from('<f', newestData, 1))
            yac = eval("%1.6f" % struct.unpack_from('<f', newestData, 5))
            zac = eval("%1.6f" % struct.unpack_from('<f', newestData, 9))
        elif(id==99):
            tilt = eval("%1.6f" % struct.unpack_from('<f', newestData, 1))+1.57
            vel = eval("%1.6f" % struct.unpack_from('<f', newestData, 5))
            roll = eval("%1.6f" % struct.unpack_from('<f', newestData, 9))
        elif(id==4): #using gyroscope to get angular velocities
            xvel = eval("%1.6f" % struct.unpack_from('<f', newestData, 1))
            yvel = eval("%1.6f" % struct.unpack_from('<f', newestData, 5))
            zvel = eval("%1.6f" % struct.unpack_from('<f', newestData, 9))            

        xvel=getMovement(xvel,sensx)
        yvel=getMovement(yvel,sensy)
        zvel=getMovement(zvel,sensz)

        if(xvel!=0 and yvel!= 0 and zvel!=0):
            print("%.2f" % xvel, "%.2f" % yvel, "%.2f" % zvel)
            pyautogui.FAILSAFE=False
            pyautogui.moveRel(-zvel*100,-xvel*100)
            


