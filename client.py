from TcpServer import TcpServer






if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000

    server = TcpServer(host, port, "client")

    msg = input(" -> ")
    while msg != "quit" or msg != "exit" or msg != "q":
        server.send(msg)
        print("waiting for response")
        data = server.receive()
        if data:
            print ('Received from server: ' + data)
        else:
            print("No response")
         
        msg = input(" -> ")