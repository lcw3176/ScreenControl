from tkinter import *
from PIL import Image, ImageTk
from socket import *
import pyautogui
import io

width, height = pyautogui.size()


class ScreenScan:
    def __init__(self, win):
        self.win = win
        self.can = Canvas(self.win, width=width, height=height)
        self.can.pack()
        self.controlButton = Button(self.win, text='Remote', bg='white', command=self.remote)
        self.controlButton.place(x=width - 80, y=height - 80, width=80, height=30)
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(('', 3000))
        self.connectionSock = ''
        self.data = []
        self.win.bind('<KeyPress>', self.keyboardControl)
        self.can.bind('<Button-1>', self.mousePosition)
        self.can.bind('<Button-3>', self.mousePosition)
        self.run = False
        self.access = False  # default: False
        self.status = False
        self.clientDisplay = []  # [0] 가로 [1] 세로
        self.x = None
        self.y = None

    def mousePosition(self, event):
        if self.access:
            x = int(int(self.clientDisplay[0]) / width * event.x)
            y = int(int(self.clientDisplay[1]) / height * event.y)
            coord = str(x) + ':' + str(y) + ':' + str(event.num)
            self.connectionSock.send(coord.encode('utf-8'))

    def remote(self):
        Label(self.win, text='Controlln', font='bold 15').place(x=10, y=10)
        self.access = True

    def keyboardControl(self, event):
        if self.access:
            input = event.keysym
            if input == 'Shift_R' or input == 'Shift_L':
                self.connectionSock.send('shift'.encode('utf-8'))
            elif input == 'Alt_L':
                self.connectionSock.send('enter'.encode('utf-8'))
            else:
                self.connectionSock.send(input.encode('utf-8'))

    def connect(self):
        while True:
            try:
                self.serverSock.listen(10)
                self.connectionSock, _ = self.serverSock.accept()
                self.clientDisplay.append(self.connectionSock.recv(4).decode('utf-8'))
                self.clientDisplay.append(self.connectionSock.recv(4).decode('utf-8'))
                break
            except OSError or ConnectionResetError:
                continue

    def receive(self):
        length = self.connectionSock.recv(9).decode('utf-8')
        length = int(length.rstrip('*'))
        temp = []
        byte = 0
        while byte < length:
            chunk = self.connectionSock.recv(length - byte)
            temp.append(chunk)
            byte = byte + len(chunk)
        return b''.join(temp)

    def main(self):
        while True:
            b = Image.open(io.BytesIO(self.receive()))
            data = ImageTk.PhotoImage(b)
            self.can.create_image(0, 0, anchor=NW, image=data)
            self.win.update()


root = Tk()
root.geometry(str(width) + 'x' + str(height))
root.resizable(False, False)
root.attributes('-fullscreen', True)
root.title('ScreenScan')
screen = ScreenScan(root)


if __name__ == '__main__':
    screen.connect()
    screen.main()
    root.mainloop()
