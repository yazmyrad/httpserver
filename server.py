import socket
import re
import os
import threading
from apidata import geo_data, weather_data
import json

header_re = re.compile(r"(GET|POST) ([^ ]+) HTTP/", re.I)

def status(code):
    if code == 200:
        return "200 OK"
    elif code == 404:
        return "404 Not Found"

def response(code, data, mime = "text/plain", headers = None):
    response_headers = {
        "Server": "Python",
        "Content-Type": mime,
        "Content-Length": len(data),
        "Connection": "close"
    }
    if headers:
        response_headers.update(headers)
    headers = "\r\n".join([ "%s: %s" % (k,v) for k, v in response_headers.items()])
    res = "HTTP/1.1 %s\r\n%s\r\n\r\n%s"
    return res % (status(code), headers, data)

def mime(fname):
    ext = os.path.splitext(fname)[1]
    if ext == '.html':
        return 'text/html'
    elif ext == '.js':
        return 'application/javascript'
    elif ext == '.jpg':
        return 'image/jpeg'
    elif ext == ".png":
        return 'image/png'
    elif ext == '.css':
        return 'text/css'
    elif ext == '.ico':
        return 'image/vnd.microsoft.icon'
    elif fname == 'weather-content':
        return 'application/json'
    else:
        return 'text/plain'

def get_request_data(socket):
    request = []
    while True:
        data = socket.recv(100).decode()
        request.append(data)
        if len(data) < 100:
            break
    return "".join(request).split("\r\n\r\n", 1)

def handler(socket):
    global header_re
    request = get_request_data(socket)
    print(request)
    m = re.search(header_re, request[0])
    if m:
        root = os.getcwd()
        print(root)
        matches = m.groups()
        if matches[1] == "/":
            fname = "index.html"
        else:
            fname = matches[1][1:]
        print(fname)
        path = os.path.join(root, fname)
        print(path)
        if os.path.exists(path):
            if matches[0] == "HEAD":
                content = ""
            else:
                content = open(path, encoding='utf-8').read()
            socket.send(response(200, content, mime(fname)).encode())
        elif fname == 'weather-condition':
            geo = geo_data()
            content = None
            if geo != None:
                content = weather_data(geo[0], geo[1])
            if content != None: 
                socket.send(response(200, json.dumps(content), mime(fname)).encode())
            else:
                socket.send(response(404, "404 Page Not found").encode())
        else:
            if matches[0] == "HEAD":
                content = ""
            else:
                content = "404 Page Not found"
            socket.send(response(404, content).encode())
    socket.close()

if __name__ == '__main__':
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", 8080))
        server.listen(5)
        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target = handler, args=(client,))
            client_handler.start()
    except KeyboardInterrupt:
        server.close()