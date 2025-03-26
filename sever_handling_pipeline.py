import win32file
import win32pipe

PIPE_NAME = r'\\.\pipe\MyPipe'
pipe=None
MAX_MESSAGE_SIZE = 64*1024
class server_handler:
    
    @staticmethod
    def run_server()->bool:
        global pipe
        pipe = win32pipe.CreateNamedPipe(
            PIPE_NAME,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1,
            MAX_MESSAGE_SIZE,
            MAX_MESSAGE_SIZE, 
            300, 
            None
        )

        print("Waiting for client connection...")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("Client connected!")
        return True
    
    @staticmethod
    def receive_initial_message()->str: 
        result, data = win32file.ReadFile(pipe, MAX_MESSAGE_SIZE)
        initiate_message = data.decode('utf-8')
        return initiate_message
    
    @staticmethod
    def send_request( message:str):  
        win32file.WriteFile(pipe, message.encode('utf-8'))
        result, data = win32file.ReadFile(pipe, MAX_MESSAGE_SIZE)
        response = data.decode('utf-8')
        return response
    
    @staticmethod
    def send_end_message( message:str):
        win32file.WriteFile(pipe, message.encode('utf-8'))


if __name__ == "__main__":
    server_handler.run_server()
    #print(initiate_message)
    reposnse=server_handler.send_request('hi')
    #print(reposnse)
