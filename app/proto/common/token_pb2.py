# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: common/token.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'common/token.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from app.proto.common import common_pb2 as common_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63ommon/token.proto\x12\x06\x63ommon\x1a\x13\x63ommon/common.proto\"m\n\x11JustTokenResponse\x12\x0f\n\x05token\x18\x01 \x01(\tH\x00\x12\x36\n\x0e\x65rror_response\x18\x02 \x01(\x0b\x32\x1c.common.DefaultErrorResponseH\x00\x42\x0f\n\rtokenResponse\"3\n\x14TokenWithTextSuccess\x12\r\n\x05token\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\"\x82\x01\n\rTokenWithText\x12/\n\x07success\x18\x01 \x01(\x0b\x32\x1c.common.TokenWithTextSuccessH\x00\x12\x36\n\x0e\x65rror_response\x18\x02 \x01(\x0b\x32\x1c.common.DefaultErrorResponseH\x00\x42\x08\n\x06result\"\x88\x01\n\x14TokenAndUserResponse\x12,\n\x08response\x18\x01 \x01(\x0b\x32\x18.common.TokenAndUserDataH\x00\x12\x36\n\x0e\x65rror_response\x18\x02 \x01(\x0b\x32\x1c.common.DefaultErrorResponseH\x00\x42\n\n\x08Response\"\xb0\x01\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08language\x18\x03 \x01(\t\x12\r\n\x05theme\x18\x04 \x01(\t\x12\x11\n\tbirthdate\x18\x05 \x01(\t\x12\x0f\n\x07\x63redits\x18\x06 \x01(\x05\x12\x12\n\nlast_login\x18\x07 \x01(\t\x12\x12\n\nphoto_link\x18\x08 \x01(\t\x12\x0b\n\x03sex\x18\t \x01(\t\x12\x11\n\tpronounce\x18\n \x01(\t\"=\n\x10TokenAndUserData\x12\r\n\x05token\x18\x01 \x01(\t\x12\x1a\n\x04user\x18\x02 \x01(\x0b\x32\x0c.common.Userb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.token_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_JUSTTOKENRESPONSE']._serialized_start=51
  _globals['_JUSTTOKENRESPONSE']._serialized_end=160
  _globals['_TOKENWITHTEXTSUCCESS']._serialized_start=162
  _globals['_TOKENWITHTEXTSUCCESS']._serialized_end=213
  _globals['_TOKENWITHTEXT']._serialized_start=216
  _globals['_TOKENWITHTEXT']._serialized_end=346
  _globals['_TOKENANDUSERRESPONSE']._serialized_start=349
  _globals['_TOKENANDUSERRESPONSE']._serialized_end=485
  _globals['_USER']._serialized_start=488
  _globals['_USER']._serialized_end=664
  _globals['_TOKENANDUSERDATA']._serialized_start=666
  _globals['_TOKENANDUSERDATA']._serialized_end=727
# @@protoc_insertion_point(module_scope)
