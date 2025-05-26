import grpc

from app.proto.user import authRouter_pb2_grpc
from app.proto.user import authRouter_pb2

def grpc_login(login: str, password: str):
    try:
        with grpc.insecure_channel('localhost:50526') as channel:
            stub = authRouter_pb2_grpc.AuthServiceStub(channel)
            request = authRouter_pb2.LoginRequest(login=login, password=password)
            response = stub.Login(request)
            print(f"[✔] Token received: {response.token}")
            return response.token
    except grpc.RpcError as e:
        print(f"[✘] Login failed: {e.details()}")
        return None
