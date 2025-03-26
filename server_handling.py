import socket
import threading
import queue
import logging

class server_handler:
    client_socket=None
    result_queue = queue.Queue()
    def __init__(self) -> None:
        self.create_server_logger()

    def create_server_logger(self):
        self.logger = logging.getLogger('server_handler_logger')
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('server_handler_log.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    def run_server(self):
        global client_socket
        # create a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 12345
        server_ip = socket.gethostbyname(socket.gethostname())  # localhost
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        thread = threading.Thread(target=self.initiate_receive_message, args=(" ",client_socket))# client_socket has to be passed within the current thread task
        thread.start()
        #self.log_queue_contents("Before getting initial message") ##Queue before 
        initiate_message= self.result_queue.get()
        #self.log_queue_contents("After getting initial message")  ##Queue after 
        return initiate_message

    def initiate_receive_message(self, message, client_socket):
        response=client_socket.recv(4096).decode("utf-8")#User Input 
        # Debugging statement
        #print(f"Initial message received: {response}")
        #self.log_queue_contents("Before put initial message") ##Queue before 
        self.result_queue.put(response)
        #self.log_queue_contents("After put initial message in queue") ##Queue after 

    def send_info(self, message):
        thread = threading.Thread(target=self.send, args=(message,client_socket))# client_socket has to be passed within the current thread task
        thread.start()


    def send_request(self, message):  
        #self.log_queue_contents("Before get on send_request") ##Queue before 
        thread = threading.Thread(target=self.send, args=(message,client_socket))# client_socket has to be passed within the current thread task
        thread.start()
        result = self.result_queue.get()
        #print(f"Result from send_request: {result}")  # Debugging statement
        #self.log_queue_contents("After get response on send_request") ##Queue after 
        return result


    def send(self, message, client_socket):
        try:
            if isinstance(message, str):  # Ensure message is in bytes
                client_socket.send(message.encode("utf-8"))
            else:
                client_socket.send(message)
            response = client_socket.recv(4096).decode("utf-8")
            #print(f"Response received in SEND: {response}") # Debugging statement
            #self.log_queue_contents("Before put response in queue for send") ##Queue before 
            self.result_queue.put(response)
            #self.log_queue_contents("After put response in queue for send") ##Queue after 
        except BrokenPipeError:
            print("Error: Broken Pipe - Client disconnected unexpectedly")

    def close_server(self):
        if client_socket:
            client_socket.close()

    def log_queue_contents(self, context):
        print(f"{context}: Queue contents: {[self.result_queue.queue[i] for i in range(self.result_queue.qsize())]}")
        
#--------------Test Main---------------------
if __name__ == "__main__":
    handler= server_handler()
    initiate_message=handler.run_server()
    #print(initiate_message)
    reposnse=handler.send_request('hi')
    #print(reposnse)