import os
import socket
from PIL import Image, ImageOps, ImageTk
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import psutil
import time
import threading


# There is a thread t1 that switches between images
# This exit event is a check to know whether the thread should be terminated or not
exit_event = threading.Event()

##### FUNCTION TO TAKE IMAGE INPUT IN THE VARIABLES filename1 and filename2 #####

def imageInput(client_socket, BUFFER_SIZE, filename1, filename2):
    try:
        # removing filename1 from previous iteration
        os.remove(filename1)
    except:
        pass

    with open(filename1, "wb") as f1:
        while True:
            bytes_read = client_socket.recv(1024)
            if bytes_read == b'n':
                break
            if not bytes_read:
                break
            f1.write(bytes_read)

    print("file1 received")
    client_socket.send(b"recf1")

    try:
        # removing filename2 from previous iteration
        os.remove(filename2)
    except:
        pass

    with open(filename2, "wb") as f2:
        while True:
            bytes_read = client_socket.recv(1024)
            if bytes_read == b'nex':
                break
            if not bytes_read:
                break
            f2.write(bytes_read)

    print("file2 received")
    client_socket.send(b"recf2")

    return

##### SWITCH AND DISPLAY FUNCTIONS #####

def switch(filename1, filename2):

    # switching the functions and forming an infinite loop
    while True:
        if exit_event.is_set():
            print("reached")
            break
        display(filename1)
        if exit_event.is_set():
            break
        display(filename2)

def display(filename1):
    im1 = Image.open(filename1, mode='r')
    width = 1358
    height = 700
    im1_new = im1
    # resizing the image to fit screen
    im1 = im1.resize((width, height))
    im1_new = ImageOps.fit(im1, (width,height), method=0, bleed=0.0, centering=(0.5,0.5))
    im1_new.show()
    # denotes the time for which a particular image will be displayed
    time.sleep(20)
    # closing images
    im1_new.close()
    im1.close()
    # code to kill all display  windows
    try:
        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()
    except:
        pass

########################################

filename1 = ""
filenam2 = ""
im1 = None
im1_new = None

# DEVICE IP ADDRESS AND PORT
SERVER_HOST = "192.168.43.222"
print("IP: " + str(SERVER_HOST))
SERVER_PORT = 5002

# receive 1024 bytes every line
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

# create server tcp socket
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

# boolean variable to not set exit event for the very first connection
myFlag = False
    
print("[*] Listening as " + str(SERVER_HOST) + ":" + str(SERVER_PORT))
s.listen(1)
while True:
    try:
        # accepting new connections
        client_socket, address = s.accept()
        try:
            if(myFlag == True):
                # sets the exit event ; Thread t1 trerminates when the exit_event is set
                exit_event.set()
            else:
                # ensures that the exit event would be set for all connections after the first one
                myFlag = True

            # joining t1 thread to the main thread
            print("Closing thread")
            t1.join()
            print("Closed thread")
            # clearing the exit event to ensure that subsequent connection iamges are displayed
            exit_event.clear()
        except:
            pass

        try:
            # killing all open image displays
            for proc in psutil.process_iter():
                if proc.name() == "display":
                    proc.kill()
        except:
            pass
        try:
            # removing filenames from previous iteration
            os.remove(filename1)
            os.remove(filename2)
        except:
            pass
 
        with client_socket:
            print('Connected by ', address)
            # receiving necessary parameters from client
            received = client_socket.recv(BUFFER_SIZE).decode("utf-16")
            shutdown, filename1, filesize1, filename2, filesize2 = received.split(SEPARATOR)
            # acknowledging receieved parameters
            client_socket.send(b'rec')

            # checking if the client wants to shut the system down
            if(shutdown == "True"):
                for image in os.listdir(os.getcwd()):
                    if(image.endswith('.png') or image.endswith('.jpeg') or image.endswith('.jpg')):
                        os.remove(image)
                os.system("shutdown now -h")
            else:
                # storing filenames and filesizes
                filename1 = os.path.basename(filename1)
                filesize1 = int(filesize1)
                filename2 = os.path.basename(filename2)
                filesize2 = int(filesize2)
                # gathering image inputs for receieved files
                imageInput(client_socket, BUFFER_SIZE, filename1, filename2)
                print("hey")
                # Defining thread t1 to switch between the two images
                t1 = threading.Thread(target = switch, args = (filename1, filename2, ))
                # starting thread t1
                t1.start()
    finally:
        # closing the socket
        client_socket.close()

s.close()
