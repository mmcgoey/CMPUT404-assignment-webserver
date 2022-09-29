#  coding: utf-8 
from cgitb import html
import socketserver
import os

import codecs
from datetime import datetime

# Copyright 2022 Abram Hindle, Eddie Antonio Santos, Mark McGoey
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    def get_html(self,filetype):
        try:
            directory = os.getcwd()

            current_directory = os.getcwd()

            now = datetime.now()

            current_date = now.strftime("%A %d, %m %Y %H:%M:%S GMT")
            
            
            
            # if the request ask for the root directory then go to index.html
            if filetype == '/':
                filetype = '/index.html'
            
            
            if os.path.exists(directory +'/www'):
                directory = directory + '/www' +str(filetype)
            else:
                print("The directory www does not exist")
            
            

            
            # adding index.html to path if the path ends with /
            if directory[len(directory)-1] == '/':
                
                directory += 'index.html'

                # removing any unallowed characters using normpath
                directory = os.path.normpath(directory)
                
            else:
                # removing any unallowed characters
                directory = os.path.normpath(directory)
                
            # normpath may seperate the path into two parts so I am adding the seperated part to the original path
            if current_directory not in directory:
                current_directory += directory
                directory = current_directory

            
            


            if ('.css' not in directory) and  ('.html' not in directory) and (directory[len(directory)-1] != '/') and (os.path.exists(directory)) and os.path.isdir(directory):

                
                directory += '/index.html'

                location = 'http://127.0.0.1:8080' + filetype +"/"
                
                response = 'HTTP/1.1 301 Moved Permanently\r\nServer: Marks server\r\nDate: %s\r\nConnection: keep-alive\r\nLocation: %s\r\n\r\n'%(current_date,location)
                
                
                
                self.request.sendall(response.encode())

            
            
           
            file_read = codecs.open(directory,"r","utf-8")
            
            content = file_read.read()
            
            file_read.close()

            file_size = os.path.getsize(directory)

            
            if '.css' in directory:
                
                
                
                
                response2 = 'HTTP/1.1 200 OK\r\nServer: Marks server\r\nConnection: keep-alive\r\nContent-Type: text/css; charset=UTF-8\r\nDate:%s\r\nContent-Length: %d\r\n\r\n'%(current_date,file_size) + content

                
                self.request.sendall(bytearray(response2,'utf-8'))    
            elif '.html' in directory:
                
                
                response2 = 'HTTP/1.1 200 OK\r\nServer: Marks server\r\nConnection: keep-alive\r\nContent-Type: text/html; charset=UTF-8\r\nDate:%s\r\nContent-Length: %d\r\n\r\n'%(current_date,file_size) + content
                
                self.request.sendall(bytearray(response2,'utf-8'))    
            else:
                
                response2 =  'HTTP/1.1 200 OK\r\nServer: Marks server\r\nConnection: keep-alive\r\n\r\n' + content

                self.request.sendall(bytearray(response2,'utf-8'))
                   
        except FileNotFoundError:
            
            if '.css' in directory:
                response2 = 'HTTP/1.1 404 Not FOUND!\r\nServer: Marks server\r\nConnection: close\r\nContent-Type: text/css\r\nDate: %s\r\n\r\n'%(current_date)
            elif '.html' in directory:
                response2 = 'HTTP/1.1 404 Not FOUND!\r\nServer: Marks server\r\nConnection: close\r\nContent-Type: text/html\r\nDate:%s\r\n\r\n'%(current_date)
            else:
                response2 = 'HTTP/1.1 404 Not FOUND!\r\nServer: Marks server\r\nConnection: close\r\nDate:%s\r\n\r\n'%(current_date)

            self.request.sendall(bytearray(response2,'utf-8'))
            

    def handle_405(self,request_type):
        if request_type != 'GET':
            response2 =  'HTTP/1.1 405 Method Not Allowed\r\n\r\n' 
            self.request.sendall(bytearray(response2,'utf-8')) 



       

    


    
    def handle(self):
        self.data = self.request.recv(1024).strip()  
        print ("Got a request of: %s\n" % self.data)
        split_list = self.data.decode().split('\n')
        filename = split_list[0].split()[1]
        requestname = split_list[0].split()[0]
        
        self.handle_405(requestname)
        self.get_html(filename)

        
        
        

  



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
