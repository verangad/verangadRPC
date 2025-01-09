from __future__ import print_function

import logging
import threading

import grpc
import messenger_pb2
import messenger_pb2_grpc

"""
Client
- Client class for the messenger
"""


class Client():
    """
    Constructor
    - self.in_chatroom - status of client -> if in chatroom or not
    - self.curr_chatroom_name - name of chatroom user is currently in, if any
    - self.user - user object of the client
    """

    def __init__(self):
        self.in_chatroom = False
        self.curr_chatroom_name = ""
        self.user = None

    """
    initialize_client
    - Takes in the messenger stub, returns None
    - Prompts the user for their name, which will be the display name of the client. 
    - Sends an initialization request to the server and receives a unique ID
    - Sets the user object to the name and id
    - Starts a thread for polling chatroom messages
    """

    def initialize_client(self, stub):
        # Prompt for name, get unique ID from server and set User object
        name = input("Enter your name: ")
        resp = stub.initialize_client(messenger_pb2.Empty())
        self.user = messenger_pb2.User(id=resp.id, name=name, chatroomId=-1)

        # Start thread
        threading.Thread(target=self.poll_message, args=(stub,), daemon=True).start()

    """
    make_message
    - Takes in a string and creates a message object using the Client ID and name and returns it.
    """

    def make_message(self, message):
        return messenger_pb2.Message(
            chatroomId=self.user.chatroomId,
            user=self.user,
            message=message
        )

    """
    get_chatrooms
    - Takes in the messenger stub, returns the list of chatrooms requested from the server.
    - Sends an empty message to the server to get a list of chatrooms
    """

    def get_chatrooms(self, stub):
        chatrooms = stub.get_chatrooms(messenger_pb2.Empty())
        return chatrooms

    """
    get_chatrooms
    - Takes in the messenger stub and an integer representing the chatroomId to join
    - Returns the response from the server. 
        - If resp == -1 -> invalid chatroom. 
        - If resp == 0 -> chatroom is full
        - If resp > 0 -> successfully joined.
    - Sends a JoinChatroomRequest object to the server containing the chatroom ID and user object.
    """

    def join_chatroom(self, stub, chatroom_id):

        response = stub.join_chatroom(messenger_pb2.JoinChatroomRequest(chatroomId=chatroom_id, user=self.user))

        return response

    """
    portal_command
    - Takes in the messenger stub and a string representing the command to process.
    - Returns None. 
    - Parses commands given in the Client portal and calls the appropriate method to send the request.
        - gc -> get chatroom
        - get chatrooms -> get chatroom
        - gcu -> get chatroom list with users
        - get chatrooms users -> get chatroom list with users
        - j -chatroomid -> join chatroom
        - join -chatroomid -> join chatroom
        - help -> view commands
        - c -chatroomname -> create chatroom
        - create -chatroomname -> create chatroom
    """

    def portal_command(self, stub, command):

        # Parse list chatrooms
        if command == "gc" or command == "get chatrooms" or command == "gcu" or command == "get chatrooms users":

            # Request chat list from server
            # Chatroom object has list of names, id, users, and capacity.
            response = self.get_chatrooms(stub)

            # Print details. If chatroom array response has no chatrooms, print "No available chatrooms."
            print("\n----------- Chatroom Directory -----------\n")

            if len(response.chatrooms) == 0:
                print("No available chatrooms.\n")

            else:
                # Chatrooms found, loop through and print
                # Print name and chatroomId
                for chatroom in response.chatrooms:
                    print("Name: ", chatroom.name)
                    print("ChatroomId: ", chatroom.id)

                    # If gcu is called -> print capacity and user list
                    if command == "gcu" or command == "get chatrooms users":
                        print("Capacity: " + str(len(chatroom.users)) + "/" + str(chatroom.capacity))
                        for user in chatroom.users:
                            print("\t|- " + user.name + " (Id: " + str(user.id) + ")")

                    print("\n")

        # Parse join chatroom command
        elif command.startswith("j ") or command.startswith("join "):

            # Get requested chatroom id from the command
            if command.startswith("j "):
                chatroom_request_id = command.removeprefix("j ")
            else:
                chatroom_request_id = command.removeprefix("join ")

            try:
                # Send request to join chatroom
                response = self.join_chatroom(stub, int(chatroom_request_id))

                # Parse response
                chatroom_id = response.chatroomId
                chatroom_name = response.chatroomName

                # Valid join, print messages and set variables to be in a chatroom
                if chatroom_id > 0:
                    print("Joined chatroom " + str(chatroom_id) + ": " + chatroom_name)
                    print("Type ':leave; to leave the chatroom")
                    print("\n----------- " + chatroom_name + " -----------\n")
                    self.user.chatroomId = chatroom_id
                    self.curr_chatroom_name = chatroom_name
                    self.in_chatroom = True

                # Chatroom is full, print message
                elif chatroom_id == 0:
                    print("Chatroom is full.")
                # Chatroom does not exist, print message
                else:
                    print("Chatroom does not exist.")
            except:
                print("Given chatroomId must be an integer.")

        # Parse create chatroom command
        elif command.startswith("c ") or command.startswith("create "):

            # Get requested chatroom name from the command
            if command.startswith("c "):
                chatroom_name = command.removeprefix("c ")
            else:
                chatroom_name = command.removeprefix("create ")

            # Send request to create chatroom and print the message that the chatroom has been created
            new_chatroom = stub.create_chatroom(messenger_pb2.CreateChatroomRequest(chatroomName=chatroom_name))
            print("Created Chatroom " + new_chatroom.name + " (id: " + str(new_chatroom.id) + ")")

        # Print help chatroom command
        elif command == "help":
            print("\n----------- Help -----------\n")
            print("View chatrooms: gc")
            print("View chatrooms with capacity and user lists: gcu")
            print("Join chatroom: j -chatroomId")
            print(
                "\t-chatroomId is the Id of the chatroom to join. You may join the chatroom if it has available capacity.")
            print("\tex) j 1")
            print("Create chatroom: c -chatroomName")
            print(
                "\t-chatroomName is the name of the chatroom to create. Names may not be unique as chatrooms are assigned a unique Id.")
            print("\tex) c My Chatroom\n")

        else:
            print("Invalid Command. Enter 'help' for help.")

    """
    send_message
    - Takes in the messenger stub and returns None.
    - This method runs in a loop after the connection is made and initialization is complete.
    """

    def send_message(self, stub):

        # Loop for input
        while True:

            # If in Client Portal -> take and parse commands
            if not self.in_chatroom:
                message = input(self.user.name + " - No chatroom: ")
                self.portal_command(stub, message)

            # If in Chatroom -> send messages or check for ":leave" command
            else:
                message = input()

                # Command ":leave" to send a leave chatroom request
                if message == ":leave":
                    response = stub.leave_chatroom(
                        messenger_pb2.LeaveChatroomRequest(chatroomId=self.user.chatroomId, user=self.user))

                    # Set Client status to "not in chatroom"
                    self.in_chatroom = False
                    self.user.chatroomId = -1
                    self.curr_chatroom_name = ""
                    print(response)

                # If message is not to leave -> create a message object with the input message and send it to the server
                # to be added to the chat list
                stub.send_message(self.make_message(message))

    """
    poll_message
    - Takes in the messenger stub and returns None.
    - This method runs in a loop after the connection is made, initialization is complete, and while the Client is in a Chatroom.
    - This method polls and sends requests to the server to check if any new messages have been sent to the Chatroom from other clients.
    - It then prints the recieved messages.
    """

    def poll_message(self, stub):

        # Loop
        while True:

            # Loop through messages recieved from poll_msg() and print any received
            for message in stub.poll_message(self.user):
                # Update index so server knows that we have already received the message
                self.user.chatIndex = message.index + 1
                print(message.user.name + " (" + str(message.user.id) + "): " + message.message, flush=True)


"""
run
- Starts the client and connects to the server at port 50051
"""


def run():
    # Start connection, terminates when connection ends
    with grpc.insecure_channel("localhost:50051") as channel:
        # Create client and stub
        client = Client()
        stub = messenger_pb2_grpc.MessengerStub(channel)

        # Make the initial request to the server to the get unique ID of the client
        client.initialize_client(stub)

        # Start the loop to check for client input
        print("----------- Messenger Portal -----------\n")
        client.send_message(stub)


# Main method, calls the run() method to start the client and connect to the server
if __name__ == "__main__":
    logging.basicConfig()
    run()
