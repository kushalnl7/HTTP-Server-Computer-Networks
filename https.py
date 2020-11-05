import socket
import sys
import os
import datetime
import time
"""
HTTP/1.1 200 OK
Date: Mon, 12 Oct 2020 06:35:24 GMT
Server: Apache/2.4.41 (Ubuntu)
Last-Modified: Tue, 06 Oct 2020 13:33:34 GMT
ETag: "2aa6-5b100a5427dfe"
Accept-Ranges: bytes
Content-Length: 10918
Vary: Accept-Encoding
Content-Type: text/html
"""

x = datetime.datetime.now()
headers = {
        'Date': "%s, %s GMT" % (x.strftime("%A")[:3], x.strftime("%d %b %Y %H:%M:%S")),
        'Server': 'CrudeServer',
        'Last-Modified': 'Tue, 06 Oct 2020 13:33:34 GMT',
        'ETag': "2aa6-5b100a5427dfe",
        'Accept-Ranges': 'bytes',
        'Content-Length': '10918',
        'Vary': 'Accept-Encoding',
        'Content-Type': 'text/html',
          }
status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
        400: 'Bad Request',
        201: 'Created',
        202: 'Accepted',
         }

def response_line(status_code):
    """Returns response line"""
    reason = status_codes[status_code]
    return "HTTP/1.1 %s %s\r\n" % (status_code, reason)

def response_headers(l = None, date = None, filename = None):
    """Returns headers
    The `extra_headers` can be a dict for sending 
    extra headers for the current response
    """
    #headers_copy = headers.copy() # make a local copy of headers

    #if extra_headers:
        #headers_copy.update(extra_headers)

    header = ""
    for h in headers:
        if(h == 'Content-Length'):
            header += "%s: %s\r\n" % (h, l)
        # elif(h == 'Last-Modified'):
            # header += "%s: %s\r\n" % (h, time.ctime(os.path.getmtime(filename)))
        elif(h == 'Date' and date != None):
            header += date
        else:
            header += "%s: %s\r\n" % (h, headers[h])
    return header


    

def HTTP_400_Handler():
    responseline = response_line(status_code=400)
    response_body = "<h1>400 Bad Request</h1>\n"
    l = len(response_body)
    responseheaders = response_headers(l)
    blank_line = "\r\n"
    
    return "%s%s%s%s%s" % (
        blank_line,
        responseline,
        responseheaders,
        blank_line,
        response_body
    )


def HTTP_501_handler(uri):
    responseline = response_line(status_code=501)
    blank_line = "\r\n"
    response_body = "<h1>501 Not Implemented</h1>\n"
    l = len(response_body)
    responseheaders = response_headers(l)
    return "%s%s%s%s%s" % (
            blank_line,
            responseline, 
            responseheaders, 
            blank_line, 
            response_body
        )

def OPTIONS(uri):
    responseline = response_line(200)
    extra_headers = {'Allow': 'OPTIONS, GET'}
    responseheaders = response_headers()
    blank_line = "\r\n"
    return "%s%s%s%s" % (
            blank_line,
            responseline, 
            responseheaders,
            blank_line
        )

def GET(uri):
    filename = uri.strip('/') # remove the slash from URI
    if os.path.exists(filename):
        responseline = response_line(200)
        with open(filename) as f:
            response_body = f.read()
        l = len(response_body)
        date = "%s +0530" % (x.strftime("%d/%b/%Y:%H:%M:%S"))
        logtext = '%s - - [%s] "GET %s HTTP/1.1" 200 %s "-" "-" \r\n' % (host, date, filename, (os.stat(filename)).st_size)
        date = "%s, %s GMT" % (x.strftime("%A")[:3], x.strftime("%d %b %Y %H:%M:%S"))
        responseheaders = response_headers(l, date, filename)
        
        
    else:
        responseline = response_line(404)
        response_body = "<h1>404 Not Found</h1>responseheaders = response_headers(len(response_body))\n"
        l = len(response_body)
        date = "%s +0530" % (x.strftime("%d/%b/%Y:%H:%M:%S"))
        logtext = '%s - - [%s] "GET %s HTTP/1.1" 400 0 "-" "-" \r\n' % (host, date, filename)
        responseheaders = response_headers(l)
    blank_line = "\r\n"
    
    
    with open("access.log", "a") as myfile:
        myfile.write(logtext)
    return "%s%s%s%s%s" % (
            blank_line,
            responseline, 
            responseheaders, 
            blank_line, 
            response_body
        )
    
def POST(uri, data):
    lines = data.split('\r\n')
    responseline = response_line(200)
    l = len(lines[-1])
    responseheaders = response_headers(l+1)
    blank_line = "\r\n"
    k = lines[-1].split('&')
    response_body = ""
    for i in k:
        response_body += str(i) + "\r\n"
    return "%s%s%s%s%s" % (
            blank_line,
            responseline, 
            responseheaders, 
            blank_line, 
            response_body
        )
    
def HEAD(uri):
    filename = uri.strip('/') # remove the slash from URI
    if os.path.exists(filename):
        responseline = response_line(200)
        with open(filename) as f:
            response_body = f.read()
        l = len(response_body)
        date = "%s +0530" % (x.strftime("%d/%b/%Y:%H:%M:%S"))
        logtext = '%s - - [%s] "HEAD %s HTTP/1.1" 200 %s "-" "-" \r\n' % (host, date, filename, (os.stat(filename)).st_size)
        date = "%s, %s GMT" % (x.strftime("%A")[:3], x.strftime("%d %b %Y %H:%M:%S"))
        responseheaders = response_headers(l, date)
        
    else:
        responseline = response_line(404)
        response_body = "<h1>404 Not Found</h1>\n"
        l = len(response_body)
        date = "%s +0530" % (x.strftime("%d/%b/%Y:%H:%M:%S"))
        logtext = '%s - - [%s] "HEAD %s HTTP/1.1" 400 0 "-" "-" \r\n' % (host, date, filename)
        responseheaders = response_headers(l)
    blank_line = "\r\n"

    with open("access.log", "a") as myfile:
        myfile.write(logtext)
    return "%s%s%s%s" % (
            blank_line,
            responseline, 
            responseheaders, 
            blank_line, 
        )

def PUT(uri, data):
    data = data.split('\r\n')[-1]
    filename = uri.strip('/')
    if(os.path.isfile(filename) == False):
        f = open(filename,"w+")
        f.write(data)
        response_body = ""
        if(f):
            response_body += "<h1>The file was created.</h1>\n"
        blank_line = "\r\n"
        responseline = response_line(201)
        responseheaders = response_headers(len(response_body))
    else:
        f = open(filename,"w+")
        f.write(data)
        blank_line = "\r\n"
        responseline = response_line(200)
        response_body = ""
        responseheaders = response_headers(len(response_body))

    """ 204 No Content Status Code Pending """
    return "%s%s%s%s%s" % (
            blank_line,
            responseline, 
            responseheaders, 
            blank_line, 
            response_body
        )

def DELETE(uri):
    filename = uri.strip('/')
    if(os.path.isfile(filename) == False):
        """ Not Sure about 202"""
        responseline = response_line(202)
        response_body = ""
        responseheaders = response_headers(len(response_body))
    else:
        os.remove(filename)
        responseline = response_line(200)
        response_body = "<html><body><h1>File deleted.</h1></body></html>"
        responseheaders = response_headers(len(response_body))
    blank_line = "\r\n"
    """ 204 No Content Status Code Pending """
    return "%s%s%s%s%s" % (
            blank_line,
            responseline, 
            responseheaders, 
            blank_line, 
            response_body
        )

def HTTPRequest(data):
    http_version = '1.1' # default to HTTP/1.1 if request doesn't provide a version
    headers = {} # a dictionary for headers
    lines = data.split('\r\n')
    words = lines[0].split(' ')
    method = words[0]
    try:
        uri = words[1]
    except(IndexError):
        uri = None
    if len(words) > 2:
        http_version = words[2]
    return method, uri, http_version
    

def handle_request(data):
    data = data.decode()
        # print(data)
    # print("")
    method, uri, http_version = HTTPRequest(data)
    if(method == 'GET'):
        if(uri == None):
            response = HTTP_400_Handler()
        else:
            response = GET(uri)
    elif(method == 'HEAD'):
        response = HEAD(uri)
    elif(method == 'POST'):
        response = POST(uri, data)
    elif(method == 'PUT'):
        response = PUT(uri, data)
    elif(method == 'DELETE'):
        response = DELETE(uri)
    else:
         response = HTTP_501_handler(uri)
    return response

host='127.0.0.1'
try:
    port=int(sys.argv[1])
except(IndexError):
    print("Provide the port number in command line.")
    exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
print("Listening at", s.getsockname())

while True:
    conn, addr = s.accept()
    print("Connected by", addr)
    data = (conn.recv(1024))
    print(data.decode().split('\r\n')[-1])
    response = handle_request(data)
    conn.sendall(bytes(response, 'utf-8'))
    conn.close()
