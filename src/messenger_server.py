from concurrent import futures
import logging

import grpc
import messenger_pb2
import messenger_pb2_grpc

"""
MessengerServicer
- Servicer class for the messenger
"""
class MessengerServicer(messenger_pb2_grpc.Messenger):

    """
    Constructor
    - self.chatrooms - list of Chatroom objects currently in the service
    - self.id_counter - counter for assigning users unique IDs
    - self.chat_room_counter - counter for assigning chatrooms unique IDs
    """
    def __init__(self):
        self.chatrooms = messenger_pb2.ChatroomList(chatrooms=[])
        self.id_counter = 0
        self.chat_room_counter = 1
        self.max_capacity = 5

    """
    initialize_client
    - Recieves an empty message from a client and returns an InitializeResponse() object
        containing the unique id of the client.
    """
    def initialize_client(self, request: messenger_pb2.Empty, context):

        # Get unique id for the client and return it
        id = self.id_counter
        resp = messenger_pb2.InitializeResponse(id=id)

        self.id_counter = self.id_counter + 1
        return resp

    """
    create_chatroom
    - Recieves a CreateChatroomRequest from a client containing the name of the chatroom to be created
        and returns a Chatroom() object containing the details of the new Chatroom.
    """
    def create_chatroom(self, request: messenger_pb2.CreateChatroomRequest, context):

        # Get chatroom name and current id counter and create a unique chatroom
        chatroom_name = request.chatroomName
        chat_id = self.chat_room_counter
        new_chatroom = messenger_pb2.Chatroom(id=chat_id, name=chatroom_name, users=[], capacity=self.max_capacity, chats=[])

        # Add new chatroom to chatroom list
        self.chat_room_counter = chat_id + 1
        self.chatrooms.chatrooms.append(new_chatroom)
        return new_chatroom

    """
    get_chatrooms
    - Recieves a empty message from a client and returns the list of Chatrooms in the server
    """
    def get_chatrooms(self, request:  messenger_pb2.Empty, context):
        return self.chatrooms

    """
    join_chatroom
    - Recieves a JoinChatroomRequest from a client containing the unique chatroomId of the chatroom to join.
    - If the chatroom exists and is not full, then it returns a JoinChatroomResponse with the id of the chatroom and the name.
    - If the chatroom is full, the chatroomId returned is 0. If the chatroom does not exist, the chatroomId returned is -1.
    """
    def join_chatroom(self, request: messenger_pb2.JoinChatroomRequest, context):

        # RequestId, name and foundId
        chatroom_id = request.chatroomId
        found_id = -1
        chatroom_name = ""

        # Search list of chatrooms for the RequestId
        for chatroom in self.chatrooms.chatrooms:
            if chatroom.id == chatroom_id:

                # Check if there is space
                if len(chatroom.users) < int(chatroom.capacity):

                    # Add user to list of users if there is space
                    chatroom.users.append(request.user)
                    found_id = chatroom_id
                    chatroom_name = chatroom.name
                else:
                    # Chatroom is full
                    found_id = 0

        return messenger_pb2.JoinChatroomResponse(chatroomId=found_id, chatroomName=chatroom_name)

    """
    leave_chatroom
    - Recieves a LeaveChatroomRequest from a client containing the unique chatroomId of the chatroom to leave and the user object to remove from the chatroom.
    - Since leave_chatroom can only be requested in a chatroom, it simply searches the chatroom list for the chatroom,
        and removes the user from the list of users in the chatroom.
    - This method returns an empty message
    """
    def leave_chatroom(self, request: messenger_pb2.LeaveChatroomRequest, context):

        request_user = request.user
        chatroom_id = request.chatroomId

        # Search for chatroom
        for chatroom in self.chatrooms.chatrooms:
            if chatroom.id == chatroom_id:

                # Search for user in the chatroom and remove from list
                for user in chatroom.users:
                    if user.id == request_user.id:
                        chatroom.users.remove(user)

        return messenger_pb2.Empty()


    """
    poll_message
    - Recieves a User object from a client containing the current chatroomId the User is in and the index of the last message in the messsage history the user has seen.
    - poll_msg can only be requested in a chatroom and is polled by the client. poll_msg sends any new messages added to the list back to the client as a stream to be printed.
    """
    def poll_message(self, request: messenger_pb2.User, context):

        # Get current index for messages seen and chatroomId
        chat_index = request.chatIndex
        chat = request.chatroomId
        curr_chat = []

        # Find chatroom and set the current chat to be sent
        for chatroom in self.chatrooms.chatrooms:
            if chatroom.id == chat:
                curr_chat = chatroom.chats

        # Send each message in the chat starting from the current index
        while len(curr_chat) > chat_index:
            msg = curr_chat[chat_index]
            chat_index = chat_index + 1
            yield msg

    """
    send_message
    - Recieves a Message object from a client containing the current chatroomId the User is in and the message to be sent.
    - The message is added to the chatroom's chat array, which is polled by poll_msg() in the client. 
    - This returns an empty message.
    """
    def send_message(self, request: messenger_pb2.Message, context):

        # Find chatroom
        for chatroom in self.chatrooms.chatrooms:
            if chatroom.id == request.chatroomId:

                # Update index of chat and append the chat to the chatroom list of chats
                request.index = len(chatroom.chats)
                chatroom.chats.append(request)

        return messenger_pb2.Empty()

"""
serve
- Starts the server at port 50051
"""
def serve():

    # Create server and servicer
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_MessengerServicer_to_server(
        MessengerServicer(), server
    )

    # Add port and start the server
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


# Main method, calls the serve() method to start the server
if __name__ == "__main__":
    logging.basicConfig()
    serve()
