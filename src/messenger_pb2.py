# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messenger.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fmessenger.proto\x12\tmessenger\"\\\n\x07Message\x12\x12\n\nchatroomId\x18\x01 \x01(\x05\x12\r\n\x05index\x18\x02 \x01(\x05\x12\x1d\n\x04user\x18\x03 \x01(\x0b\x32\x0f.messenger.User\x12\x0f\n\x07message\x18\x04 \x01(\t\"G\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x12\n\nchatroomId\x18\x03 \x01(\x05\x12\x11\n\tchatIndex\x18\x04 \x01(\x05\"y\n\x08\x43hatroom\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x63\x61pacity\x18\x03 \x01(\x05\x12\x1e\n\x05users\x18\x04 \x03(\x0b\x32\x0f.messenger.User\x12!\n\x05\x63hats\x18\x05 \x03(\x0b\x32\x12.messenger.Message\"H\n\x13JoinChatroomRequest\x12\x12\n\nchatroomId\x18\x01 \x01(\x05\x12\x1d\n\x04user\x18\x02 \x01(\x0b\x32\x0f.messenger.User\"@\n\x14JoinChatroomResponse\x12\x12\n\nchatroomId\x18\x01 \x01(\x05\x12\x14\n\x0c\x63hatroomName\x18\x02 \x01(\t\"6\n\x0c\x43hatroomList\x12&\n\tchatrooms\x18\x01 \x03(\x0b\x32\x13.messenger.Chatroom\" \n\x12InitializeResponse\x12\n\n\x02id\x18\x01 \x01(\x05\"I\n\x14LeaveChatroomRequest\x12\x12\n\nchatroomId\x18\x01 \x01(\x05\x12\x1d\n\x04user\x18\x02 \x01(\x0b\x32\x0f.messenger.User\"-\n\x15\x43reateChatroomRequest\x12\x14\n\x0c\x63hatroomName\x18\x01 \x01(\t\"\x07\n\x05\x45mpty2\xe9\x03\n\tMessenger\x12\x46\n\x11initialize_client\x12\x10.messenger.Empty\x1a\x1d.messenger.InitializeResponse\"\x00\x12\x36\n\x0csend_message\x12\x12.messenger.Message\x1a\x10.messenger.Empty\"\x00\x12\x37\n\x0cpoll_message\x12\x0f.messenger.User\x1a\x12.messenger.Message\"\x00\x30\x01\x12R\n\rjoin_chatroom\x12\x1e.messenger.JoinChatroomRequest\x1a\x1f.messenger.JoinChatroomResponse\"\x00\x12\x45\n\x0eleave_chatroom\x12\x1f.messenger.LeaveChatroomRequest\x1a\x10.messenger.Empty\"\x00\x12J\n\x0f\x63reate_chatroom\x12 .messenger.CreateChatroomRequest\x1a\x13.messenger.Chatroom\"\x00\x12<\n\rget_chatrooms\x12\x10.messenger.Empty\x1a\x17.messenger.ChatroomList\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messenger_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MESSAGE']._serialized_start=30
  _globals['_MESSAGE']._serialized_end=122
  _globals['_USER']._serialized_start=124
  _globals['_USER']._serialized_end=195
  _globals['_CHATROOM']._serialized_start=197
  _globals['_CHATROOM']._serialized_end=318
  _globals['_JOINCHATROOMREQUEST']._serialized_start=320
  _globals['_JOINCHATROOMREQUEST']._serialized_end=392
  _globals['_JOINCHATROOMRESPONSE']._serialized_start=394
  _globals['_JOINCHATROOMRESPONSE']._serialized_end=458
  _globals['_CHATROOMLIST']._serialized_start=460
  _globals['_CHATROOMLIST']._serialized_end=514
  _globals['_INITIALIZERESPONSE']._serialized_start=516
  _globals['_INITIALIZERESPONSE']._serialized_end=548
  _globals['_LEAVECHATROOMREQUEST']._serialized_start=550
  _globals['_LEAVECHATROOMREQUEST']._serialized_end=623
  _globals['_CREATECHATROOMREQUEST']._serialized_start=625
  _globals['_CREATECHATROOMREQUEST']._serialized_end=670
  _globals['_EMPTY']._serialized_start=672
  _globals['_EMPTY']._serialized_end=679
  _globals['_MESSENGER']._serialized_start=682
  _globals['_MESSENGER']._serialized_end=1171
# @@protoc_insertion_point(module_scope)