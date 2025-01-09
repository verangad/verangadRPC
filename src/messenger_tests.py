import unittest
from concurrent import futures
import grpc
import messenger_pb2
import messenger_pb2_grpc
from messenger_server import MessengerServicer

port = 50052

class TestMessengerServicer(unittest.TestCase):

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        messenger_pb2_grpc.add_MessengerServicer_to_server(MessengerServicer(), self.server)
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

    def close(self):
        self.server.stop(None)


"""
*** Tests for initialize_client ***
"""
class TestInitializeClient(unittest.TestCase):

    def setUp(self):
        self.test_server = TestMessengerServicer()
        self.test_server.start()
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.grpc_stub = messenger_pb2_grpc.MessengerStub(self.channel)

    def tearDown(self):
        self.channel.close()
        self.test_server.close()

    def test_initialize_client_first_client(self):
        initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())

        self.assertEqual(initialize_response.id, 0)


    def test_initialize_client_multiple_clients(self):

        for i in range(0, 5):

            initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())
            self.assertEqual(initialize_response.id, i)

        initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())
        self.assertEqual(initialize_response.id, 5)

"""
*** Tests for send_message and poll_message ***
"""
class TestSendAndReceive(unittest.TestCase):

    def setUp(self):
        self.test_server = TestMessengerServicer()
        self.test_server.start()
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.grpc_stub = messenger_pb2_grpc.MessengerStub(self.channel)
        initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())
        self.user = messenger_pb2.User(id=initialize_response.id, name="TestUser1")

    def tearDown(self):
        self.channel.close()
        self.test_server.close()

    def test_send_message_to_chatroom(self):

        create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName="TestChatroom")
        self.grpc_stub.create_chatroom(create_chatroom_request)

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=1)
        join_response = self.grpc_stub.join_chatroom(join_request)

        for i in range(0, 5):
            message = messenger_pb2.Message(message="TestChat" + str(i), user=self.user, chatroomId=join_response.chatroomId)
            message_response = self.grpc_stub.send_message(message)
            self.assertEqual(message_response, messenger_pb2.Empty())

        message_polled = self.grpc_stub.poll_message(self.user)

        counter = 0
        for message in message_polled:

            self.assertEqual(message.chat, 1)
            self.assertEqual(message.user, self.user)
            self.assertEqual(message.index, counter)
            self.assertEqual(message.message, "TestChat" + str(counter))

            counter = counter + 1


    def test_send_message_to_chatroom_multiple_clients(self):
        create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName="TestChatroom")
        self.grpc_stub.create_chatroom(create_chatroom_request)

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=1)
        join_response = self.grpc_stub.join_chatroom(join_request)

        counter = 0

        for i in range(2, 5):
            temp_channel = grpc.insecure_channel(f'localhost:{port}')
            temp_initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())
            temp_user = messenger_pb2.User(id=temp_initialize_response.id, name="TestUser" + str(i))

            join_request = messenger_pb2.JoinChatroomRequest(chatroomId=1, user=temp_user)
            self.grpc_stub.join_chatroom(join_request)

            message = messenger_pb2.Message(message="TestChat From User " + str(i), user=temp_user, chatroomId=1)
            message_response = self.grpc_stub.send_message(message)
            self.assertEqual(message_response, messenger_pb2.Empty())

            message_polled = self.grpc_stub.poll_message(self.user)

            for message in message_polled:

                self.assertEqual(message.chat, 1)
                self.assertEqual(message.user, temp_user)
                self.assertEqual(message.index, counter)
                self.assertEqual(message.message, "TestChat From User " + str(i))

                counter = counter + 1

            temp_channel.close()

        for i in range(0, 5):
            message = messenger_pb2.Message(message="TestChat" + str(i), user=self.user, chatroomId=join_response.chatroomId)
            message_response = self.grpc_stub.send_message(message)
            self.assertEqual(message_response, messenger_pb2.Empty())

        message_polled = self.grpc_stub.poll_message(self.user)

        counter = 3
        for message in message_polled:
            self.assertEqual(message.chat, 1)
            self.assertEqual(message.user, self.user)
            self.assertEqual(message.index, counter)
            self.assertEqual(message.message, "TestChat" + str(counter))

            counter = counter + 1

"""
*** Tests for join_chatroom ***
"""
class TestJoinChatroom(unittest.TestCase):

    def setUp(self):
        self.test_server = TestMessengerServicer()
        self.test_server.start()
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.grpc_stub = messenger_pb2_grpc.MessengerStub(self.channel)
        initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())
        self.user = messenger_pb2.User(id=initialize_response.id, name="TestUser1")

    def tearDown(self):
        self.channel.close()
        self.test_server.close()

    def test_join_chatroom(self):

        create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName="TestChatroom")
        chatroom = self.grpc_stub.create_chatroom(create_chatroom_request)

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=chatroom.id, user=self.user)
        join_response = self.grpc_stub.join_chatroom(join_request)

        self.assertEqual(join_response.chatroomId, 1)
        self.assertEqual(join_response.chatroomName, "TestChatroom")

    def test_join_chatroom_does_not_exist(self):

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=1)
        join_response = self.grpc_stub.join_chatroom(join_request)

        self.assertEqual(join_response.chatroomId, -1)
        self.assertEqual(join_response.chatroomName, "")

        create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName="TestChatroom")
        self.grpc_stub.create_chatroom(create_chatroom_request)

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=2)
        join_response = self.grpc_stub.join_chatroom(join_request)

        self.assertEqual(join_response.chatroomId, -1)
        self.assertEqual(join_response.chatroomName, "")

    def test_join_chatroom_is_full(self):

        create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName="TestChatroom")
        self.grpc_stub.create_chatroom(create_chatroom_request)

        for i in range(2, 7):
            temp_channel = grpc.insecure_channel(f'localhost:{port}')
            temp_initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())
            temp_user = messenger_pb2.User(id=temp_initialize_response.id, name="TestUser" + str(i))

            join_request = messenger_pb2.JoinChatroomRequest(chatroomId=1, user=temp_user)
            self.grpc_stub.join_chatroom(join_request)
            temp_channel.close()

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=1,user=self.user)
        join_response = self.grpc_stub.join_chatroom(join_request)

        self.assertEqual(join_response.chatroomId, 0)
        self.assertEqual(join_response.chatroomName, "")

    def test_join_chatroom_after_leaving(self):

        create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName="TestChatroom")
        self.grpc_stub.create_chatroom(create_chatroom_request)

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=1)
        self.grpc_stub.join_chatroom(join_request)

        leave_request = messenger_pb2.LeaveChatroomRequest(chatroomId=1, user=self.user)
        self.grpc_stub.leave_chatroom(leave_request)

        join_response = self.grpc_stub.join_chatroom(join_request)

        self.assertEqual(join_response.chatroomId, 1)
        self.assertEqual(join_response.chatroomName, "TestChatroom")


"""
*** Tests for leave_chatroom ***
"""
class TestLeaveChatroom(unittest.TestCase):

    def setUp(self):
        self.test_server = TestMessengerServicer()
        self.test_server.start()
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.grpc_stub = messenger_pb2_grpc.MessengerStub(self.channel)

    def tearDown(self):
        self.channel.close()
        self.test_server.close()

    def test_leave_chatroom(self):

        initialize_response = self.grpc_stub.initialize_client(messenger_pb2.Empty())
        user = messenger_pb2.User(id=initialize_response.id, name="TestUser1")

        create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName="TestChatroom")
        chatroom = self.grpc_stub.create_chatroom(create_chatroom_request)

        join_request = messenger_pb2.JoinChatroomRequest(chatroomId=chatroom.id, user=user)
        self.grpc_stub.join_chatroom(join_request)

        get_response = self.grpc_stub.get_chatrooms(messenger_pb2.Empty())

        for chat in get_response.chatrooms:
            self.assertEqual(len(chat.users), 1)

        leave_request = messenger_pb2.LeaveChatroomRequest(chatroomId=chatroom.id, user=user)
        leave_response = self.grpc_stub.leave_chatroom(leave_request)

        self.assertEqual(leave_response, messenger_pb2.Empty())

        get_response = self.grpc_stub.get_chatrooms(messenger_pb2.Empty())

        for chat in get_response.chatrooms:
            self.assertEqual(len(chat.users), 0)


"""
*** Tests for create_chatroom ***
"""
class TestCreateChatrooms(unittest.TestCase):

    def setUp(self):
        self.test_server = TestMessengerServicer()
        self.test_server.start()
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.grpc_stub = messenger_pb2_grpc.MessengerStub(self.channel)

    def tearDown(self):
        self.channel.close()
        self.test_server.close()

    def test_create_chatroom(self):

        for i in range(0, 5):
            chatroom_name = "TestChatroom" + str(i)
            create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName=chatroom_name)
            response = self.grpc_stub.create_chatroom(create_chatroom_request)

            self.assertEqual(response.id, i + 1)
            self.assertEqual(response.name, "TestChatroom" + str(i))
            self.assertEqual(response.capacity, 5)
            self.assertEqual(len(response.users), 0)
            self.assertEqual(len(response.chats), 0)

    def test_create_chatroom_same_name(self):

        for i in range(0, 5):
            chatroom_name = "TestChatroom5"
            create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName=chatroom_name)
            response = self.grpc_stub.create_chatroom(create_chatroom_request)

            self.assertEqual(response.id, i + 1)
            self.assertEqual(response.name, "TestChatroom5")
            self.assertEqual(response.capacity, 5)
            self.assertEqual(len(response.users), 0)
            self.assertEqual(len(response.chats), 0)


"""
*** Tests for get_chatrooms ***
"""
class TestGetChatrooms(unittest.TestCase):

    def setUp(self):
        self.test_server = TestMessengerServicer()
        self.test_server.start()
        self.channel = grpc.insecure_channel(f'localhost:{port}')
        self.grpc_stub = messenger_pb2_grpc.MessengerStub(self.channel)

    def tearDown(self):
        self.channel.close()
        self.test_server.close()

    def test_get_chatrooms_no_chatrooms(self):

        response = self.grpc_stub.get_chatrooms(messenger_pb2.Empty())
        self.assertEqual(len(response.chatrooms), 0)

    def test_get_chatrooms(self):

        for i in range(0, 5):
            chatroom_name = "TestChatroom" + str(i)
            create_chatroom_request = messenger_pb2.CreateChatroomRequest(chatroomName=chatroom_name)
            self.grpc_stub.create_chatroom(create_chatroom_request)

        response = self.grpc_stub.get_chatrooms(messenger_pb2.Empty())

        self.assertEqual(len(response.chatrooms), 5)

        for i in range(0, 5):
            self.assertEqual(response.chatrooms[i].id, i + 1)
            self.assertEqual(response.chatrooms[i].name, "TestChatroom" + str(i))
            self.assertEqual(response.chatrooms[i].capacity, 5)
            self.assertEqual(len(response.chatrooms[i].users), 0)
            self.assertEqual(len(response.chatrooms[i].chats), 0)
