from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
from os import popen
import re
import cv2, imutils
from time import sleep

stream = None

class StreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('/stream.mjpg'):
            self._setupImageCanvas()
            while True:
                self._writeStream()
                sleep(0.1)
                
        elif self._checkForHomePath:
            self._setupHTML()

    def _writeStream(self):
        try:
            frame = stream.read()
            if (frame.all() != None):
                self._writeFrame(frame)
        except Exception as e:
            raise e

    def _writeFrame(self, frame):
        retval, memBuffer = cv2.imencode(".jpg", frame)
        self.wfile.write('--jpgboundary\r\n'.encode())
        self.end_headers()
        self.wfile.write(bytearray(memBuffer))

    def _checkForHomePath(self):
        return self.path.endswith('.html') or self.path == "/"

    def _setupImageCanvas(self):
        self.send_response(20)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
        self.end_headers()

    def _setupHTML(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><head></head><body>')
        self.wfile.write('<img src="http://{}:{}/stream.mjpg" height="300px" width="400px"/>'.format(stream.ipv4, stream.port).encode())
        self.wfile.write(b'</body></html>')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    "Requests are handled in the preceding thread."

class ImageStream:
    def __init__(self):
        self.frame = None
        self.isStreamEnabled = False
        self.ipv4 = self.getIP('eth0')
        self.port = 5810

    def start(self):
        self.isStreamEnabled = True
        return self

    def update(self, img):
        self.frame = img

    def read(self):
        return self.frame

    def stop(self):
        self.isStreamEnabled = False

    def getIP(self, iface):
        search_str = "ip addr show {}".format(iface)
        ipv4 = re.search(re.compile(r'(?<=inet )(.*)(?=\/)', re.M), popen(search_str).read()).groups()[0]
        return ipv4
    
def start():
    global stream

    stream = ImageStream()
    server = ThreadedHTTPServer((stream.ipv4, stream.port), StreamHandler)
    print("starting image viewer")
    Thread(target=server.serve_forever,args=()).start()
