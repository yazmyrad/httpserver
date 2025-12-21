import socket


# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)

Create a new socket object using the given address family, socket type and protocol number. 
The address family should be AF_INET (the default, IPv4 address family).
The socket type should be SOCK_STREAM (the default, TCP, basically).
"""
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
"""
    Sets socket option to allow reusing the address

    Without this, you might get "Address already in use" error when restarting the server

    socket.SOL_SOCKET: Socket-level option

    socket.SO_REUSEADDR: Allows reuse of local addresses

    1: Enables the option (True)
"""
server_socket.bind((SERVER_HOST, SERVER_PORT))
"""
    Binds the socket to a specific network interface and port

    SERVER_HOST: IP address (empty string or '0.0.0.0' for all interfaces)

    SERVER_PORT: Port number to listen on
"""
server_socket.listen(1)
"""
    Enables the server to accept connections

    1: Backlog parameter - maximum number of queued connections

    Server is now ready to accept incoming connections
"""
print('Listening on port %s ...' % SERVER_PORT)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
    """
Accept a connection. The socket must be bound to an address and listening for connections.
The return value is a pair (conn, address) where conn is a new socket object usable to send 
and receive data on the connection, and address is the address bound to the socket 
on the other end of the connection.
    """

    # Get the client request
    request = client_connection.recv(1024).decode()
    """
     socket.recv(bufsize[, flags])

Receive data from the socket. The return value is a bytes object representing the data received. 
The maximum amount of data to be received at once is specified by bufsize. 
    """
    print(request)

    # Send HTTP response
    response = 'HTTP/1.0 200 OK\n\n<h1>Hello World</h1>'
    client_connection.sendall(response.encode())
    """
 socket.sendall(bytes[, flags])

Send data to the socket. The socket must be connected to a remote socket. 
The optional flags argument has the same meaning as for recv() above. 
Unlike send(), this method continues to send data from bytes until either all data has been sent 
or an error occurs. None is returned on success. On error, an exception is raised, 
and there is no way to determine how much data, if any, was successfully sent. 
    """
    client_connection.close()

# Close socket
server_socket.close()

"""
Listening on port 8000 ...
GET / HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Priority: u=0, i


GET /favicon.ico HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
Referer: http://localhost:8000/
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
Priority: u=6
"""