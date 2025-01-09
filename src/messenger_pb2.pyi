from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message(_message.Message):
    __slots__ = ("chatroomId", "index", "user", "message")
    CHATROOMID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    chatroomId: int
    index: int
    user: User
    message: str
    def __init__(self, chatroomId: _Optional[int] = ..., index: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ..., message: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name", "chatroomId", "chatIndex")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CHATROOMID_FIELD_NUMBER: _ClassVar[int]
    CHATINDEX_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    chatroomId: int
    chatIndex: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., chatroomId: _Optional[int] = ..., chatIndex: _Optional[int] = ...) -> None: ...

class Chatroom(_message.Message):
    __slots__ = ("id", "name", "capacity", "users", "chats")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    CHATS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    capacity: int
    users: _containers.RepeatedCompositeFieldContainer[User]
    chats: _containers.RepeatedCompositeFieldContainer[Message]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., capacity: _Optional[int] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ..., chats: _Optional[_Iterable[_Union[Message, _Mapping]]] = ...) -> None: ...

class JoinChatroomRequest(_message.Message):
    __slots__ = ("chatroomId", "user")
    CHATROOMID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    chatroomId: int
    user: User
    def __init__(self, chatroomId: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class JoinChatroomResponse(_message.Message):
    __slots__ = ("chatroomId", "chatroomName")
    CHATROOMID_FIELD_NUMBER: _ClassVar[int]
    CHATROOMNAME_FIELD_NUMBER: _ClassVar[int]
    chatroomId: int
    chatroomName: str
    def __init__(self, chatroomId: _Optional[int] = ..., chatroomName: _Optional[str] = ...) -> None: ...

class ChatroomList(_message.Message):
    __slots__ = ("chatrooms",)
    CHATROOMS_FIELD_NUMBER: _ClassVar[int]
    chatrooms: _containers.RepeatedCompositeFieldContainer[Chatroom]
    def __init__(self, chatrooms: _Optional[_Iterable[_Union[Chatroom, _Mapping]]] = ...) -> None: ...

class InitializeResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class LeaveChatroomRequest(_message.Message):
    __slots__ = ("chatroomId", "user")
    CHATROOMID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    chatroomId: int
    user: User
    def __init__(self, chatroomId: _Optional[int] = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class CreateChatroomRequest(_message.Message):
    __slots__ = ("chatroomName",)
    CHATROOMNAME_FIELD_NUMBER: _ClassVar[int]
    chatroomName: str
    def __init__(self, chatroomName: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
