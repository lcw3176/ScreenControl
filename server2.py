from socket import *
import io
import wx
import pyautogui
import threading

width, height = pyautogui.size()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='ScreenScan')
        self.clientDisplay = []
        self.panel = wx.Panel(self)
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(('', 3000))
        self.connectionSock = ''
        self.image = None
        self.Bind(wx.EVT_PAINT, self.paint)
        self.panel.Bind(wx.EVT_KEY_UP, self.keyboard)
        self.panel.Bind(wx.EVT_RIGHT_DOWN, self.rightMouse)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.leftMouse)
        self.t = threading.Thread(target=self.main)
        self.ShowFullScreen(True)

    def paint(self, event):
        if self.image is not None:
            dc = wx.PaintDC(self.panel)
            dc.DrawBitmap(self.image, 0, 0)
        else:
            pass

    def leftMouse(self, event):
        x = int(int(self.clientDisplay[0]) / width * event.x)
        y = int(int(self.clientDisplay[1]) / height * event.y)
        coord = str(x) + ':' + str(y) + ':' + str('1')
        self.connectionSock.send(coord.encode('utf-8'))

    def rightMouse(self, event):
        x = int(int(self.clientDisplay[0]) / width * event.x)
        y = int(int(self.clientDisplay[1]) / height * event.y)
        coord = str(x) + ':' + str(y) + ':' + str('3')
        self.connectionSock.send(coord.encode('utf-8'))

    def keyboard(self, event):
        input = event.GetKeyCode()
        if input == wx.WXK_ESCAPE:
            self.panel.Destroy()
            self.Destroy()
        elif input == wx.WXK_RETURN:
            key = 'enter'
            self.connectionSock.send(key.encode('utf-8'))
        elif input < 256:
            key = chr(input).lower()
            self.connectionSock.send(key.encode('utf-8'))
        else:
            pass

    def connect(self):
        while True:
            try:
                self.serverSock.listen(10)
                self.connectionSock, _ = self.serverSock.accept()
                self.clientDisplay.append(self.connectionSock.recv(4).decode('utf-8'))
                self.clientDisplay.append(self.connectionSock.recv(4).decode('utf-8'))
                self.t.start()
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
            picture = wx.Image(io.BytesIO(self.receive()))
            self.image = wx.Bitmap(picture)
            self.Refresh()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.connect()
    app.MainLoop()

