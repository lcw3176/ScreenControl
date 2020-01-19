from socket import *
from PIL import ImageGrab
import io
import threading
import pyautogui
import pynput


mouse = pynput.mouse.Controller()
mouseButton = pynput.mouse.Button
keyboard = pynput.keyboard.Controller()
keyboardKey = pynput.keyboard.Key
clientWidth, clientHeight = pyautogui.size()


class ClientScan:
    def __init__(self):
        self.clientSock = ''
        self.clientPort = 3000 
        self.clientIp = '127.0.0.1' 
        self.t = threading.Thread(target=self.control)
        self.t.daemon = True

    def control(self):
        while True:
            try:
                input = self.clientSock.recv(12).decode('utf-8')
                temp = input.split(':')
                try:
                    if temp[2] == '1':
                        mouse.position = (int(temp[0]), int(temp[1]))
                        mouse.press(mouseButton.left)
                        mouse.release(mouseButton.left)
                    else:
                        mouse.position = (int(temp[0]), int(temp[1]))
                        mouse.press(mouseButton.right)
                        mouse.release(mouseButton.right)
                except IndexError:
                    try:
                        if input == 'enter':
                            keyboard.press(keyboardKey.enter)
                            keyboard.release(keyboardKey.enter)
                        else:
                            keyboard.press(input)
                            keyboard.release(input)
                    except ValueError:
                        continue
            except ConnectionResetError:
                continue
            except OSError:
                continue

    def capture(self):
        data = io.BytesIO()
        monitor = ImageGrab.grab(bbox=None)
        monitor.save(data, format='jpeg', quality=55)
        data = data.getvalue()
        length = len(str(len(data)))
        if length < 9:
            length = str(len(data)) + ((9 % length) * '*')
        self.clientSock.send(length.encode('utf-8'))
        return data

    def connect(self):
        while True:
            try:
                self.clientSock = socket(AF_INET, SOCK_STREAM)
                self.clientSock.connect((self.clientIp, self.clientPort))
                self.clientSock.send(str(clientWidth).encode('utf-8'))
                self.clientSock.send(str(clientHeight).encode('utf-8'))
                break
            except:
                continue

    def main(self):
        while True:
            try:
                raw = self.capture()
                self.clientSock.send(raw)
            except ConnectionResetError:
                self.connect()
            except OSError:
                continue


if __name__ == '__main__':
    app = ClientScan()
    app.connect()
    app.t.start()
    app.main()
