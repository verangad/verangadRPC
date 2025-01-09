## verangadRPC

This program is a messenger service with a server and a client. The messenger service has
chatrooms that can be created and joined if there is space. Clients in a chatroom can send
messages and anyone in the chatroom will receive the messages in real time. Clients can only
be in one chatroom at a time. Note that this program requires grpc to be installed.

### Given Files:
- messenger
    - messenger.proto
- messenger_client.py
- messenger_pb2.py
- messenger_pb2.pyi
- messenger_pb2_grpc.py
- messenger_server.py
- messenger_tests.py

  
### Client Portal Commands:
- gc (get chatrooms) -> Get chatrooms: Get the list of chatrooms in the server. The printed
list will contain the chatroom names and their corresponding ID.
    - Ex) gc
    - Ex) get chatrooms
- gcu (get chatrooms users) -> Get chatrooms with Users: Get the list of chatrooms in the
server with user list and capacity. The printed list will contain the chatroom names, their
corresponding IDs, and the corresponding list of Users in the chatroom and the current
capacity.
    - Ex) gcu
    - Ex) get chatrooms users
- j -chatroomId (join - chatroomId) - > Join chatroom: Request to join a chatroom with the
given ID. Users may only join a chatroom if there is space and the chatroom ID given is
valid.
    - Ex) j 123
    - Ex) join 123
- c -chatroomName (create - chatroomName) - > Create chatroom: Request to create a
chatroom with the given name. Chatroom names do not need to be unique as they are
given a unique ID.
    - Ex) c MyNewChatroom
    - Ex) create MyNewChatroom
- help -> Print out the command documentation.


### Chatroom Commands:
    - :leave -> Leave the current chatroom. This command may only the used in a chatroom
and allows the user to return to the Client Portal.


### Instructions
- To run the server in the terminal, enter:
    - python messenger_server.py
- To run an instance of a client in a different terminal, enter:
    - python messenger_client.py
    - The client should connect to the server, and you will be prompted to enter your
username:
- To run the test suite, enter:
    - Python -m unittest messenger_tests.py
