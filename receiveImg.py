import os
import socket
from PIL import Image, ImageOps, ImageTk
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import psutil

###### CODE FOR DISPLYING IMAGE ######

import sys
if sys.version_info == 2: # tkinter library reference to avoid pontential naming conflict with people's programs.
    import Tkinter
    tkinter = Tkinter
else:
    import tkinter

def showPIL(pillImg):
    root = tkinter.Tk()
    w,h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w,h))
    root.focus_set()
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    canvas = tkinter.Canvas(root, width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imWidth, imHeight = pillImg.size
    if imWidth > w or imHeight > h:
        ratio = min(w/imWidth, h/imHeight)
        imWidth = int(imWidth*ratio)
        imHeight = int(imHeight*ratio)
        pillImg = pillImg.resize((imWidth,imHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pillImg)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.mainloop()

######################################

filename = ""
im1 = None
im2 = None

# DEVICE IP ADDRESS AND PORT
SERVER_HOST = "10.42.0.41"
SERVER_PORT = 5001

# receive 4096 bytes every line
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# create server tcp socket
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
    
print("[*] Listening as " + str(SERVER_HOST) + ":" + str(SERVER_PORT))
s.listen(1)
while True:
    try:
        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()
    except:
        pass
    try:
        im2.close()
    except:
        pass
    try:
        im1.close()
    except:
        pass
    try:
        os.remove(filename)
    except:
        pass
    
    try:
        client_socket, address = s.accept()
    
        with client_socket:
            print('Connected by ', address)
            received = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            shutdown, twoImage, filename, filesize = received.split(SEPARATOR)
            print(shutdown)
            print(twoImage)
            if(shutdown == "True"):
                print("Hey1")
                os.system("shutdown now -h")
            else:
                print("Hey2")
                filename = os.path.basename(filename)
                filesize = int(filesize)
                with open(filename, "wb") as f:
                    while True:
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                    print(filename)
                    im1 = Image.open(filename)
                    width = 1350
                    height = 700
                    im2 = ImageOps.fit(im1, (width,height), method=0, bleed=0.0, centering=(0.5,0.5))
                    im2.show()
                    #showPIL(im1)
    finally:
        client_socket.close()

print("Hello world")
s.close()
