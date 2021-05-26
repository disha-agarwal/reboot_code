from simpletcp.tcpserver import TCPServer

alive = "False"
def echo(ip, queue, data):
    global alive
    data = data.decode()
    if(data == "True" or data == "False"):
        alive = data
    queue.put(alive.encode())

server = TCPServer("public", 5000, echo)
server.run()