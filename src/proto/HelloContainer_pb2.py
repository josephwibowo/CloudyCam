# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: HelloContainer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='HelloContainer.proto',
  package='HelloContainer',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14HelloContainer.proto\x12\x0eHelloContainer\"\xd4\x02\n\x0eHelloContainer\x12\x17\n\x0fProtocolVersion\x18\x01 \x02(\x05\x12\x0c\n\x04Uuid\x18\x02 \x02(\t\x12\x1e\n\x16RequireConnectedCamera\x18\x03 \x02(\x08\x12\x14\n\x0cSessionToken\x18\x04 \x01(\t\x12\x10\n\x08IsCamera\x18\x05 \x01(\x08\x12\x10\n\x08\x44\x65viceId\x18\x06 \x01(\t\x12\x11\n\tUserAgent\x18\x07 \x02(\t\x12\x18\n\x10ServiceAccessKey\x18\x08 \x01(\t\x12\x12\n\nClientType\x18\t \x02(\x05\x12\x16\n\x0eWwnAccessToken\x18\n \x01(\t\x12\x19\n\x11\x45ncryptedDeviceId\x18\x0b \x01(\t\x12\x18\n\x10\x41uthorizeRequest\x18\x0c \x03(\x0c\x12\x17\n\x0f\x43lientIpAddress\x18\r \x01(\t\x12\x1a\n\x12RequireOwnerServer\x18\x0e \x01(\x08'
)




_HELLOCONTAINER = _descriptor.Descriptor(
  name='HelloContainer',
  full_name='HelloContainer.HelloContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ProtocolVersion', full_name='HelloContainer.HelloContainer.ProtocolVersion', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Uuid', full_name='HelloContainer.HelloContainer.Uuid', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='RequireConnectedCamera', full_name='HelloContainer.HelloContainer.RequireConnectedCamera', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='SessionToken', full_name='HelloContainer.HelloContainer.SessionToken', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='IsCamera', full_name='HelloContainer.HelloContainer.IsCamera', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='DeviceId', full_name='HelloContainer.HelloContainer.DeviceId', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='UserAgent', full_name='HelloContainer.HelloContainer.UserAgent', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ServiceAccessKey', full_name='HelloContainer.HelloContainer.ServiceAccessKey', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ClientType', full_name='HelloContainer.HelloContainer.ClientType', index=8,
      number=9, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='WwnAccessToken', full_name='HelloContainer.HelloContainer.WwnAccessToken', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='EncryptedDeviceId', full_name='HelloContainer.HelloContainer.EncryptedDeviceId', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='AuthorizeRequest', full_name='HelloContainer.HelloContainer.AuthorizeRequest', index=11,
      number=12, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ClientIpAddress', full_name='HelloContainer.HelloContainer.ClientIpAddress', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='RequireOwnerServer', full_name='HelloContainer.HelloContainer.RequireOwnerServer', index=13,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=41,
  serialized_end=381,
)

DESCRIPTOR.message_types_by_name['HelloContainer'] = _HELLOCONTAINER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HelloContainer = _reflection.GeneratedProtocolMessageType('HelloContainer', (_message.Message,), {
  'DESCRIPTOR' : _HELLOCONTAINER,
  '__module__' : 'HelloContainer_pb2'
  # @@protoc_insertion_point(class_scope:HelloContainer.HelloContainer)
  })
_sym_db.RegisterMessage(HelloContainer)


# @@protoc_insertion_point(module_scope)
