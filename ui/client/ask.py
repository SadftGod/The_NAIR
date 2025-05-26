import grpc

from app.proto.chat import chat_pb2_grpc
from app.proto.chat import chat_pb2

def grpc_chat_question(query: str):
    try:
        with grpc.insecure_channel('localhost:50526') as channel:
            stub = chat_pb2_grpc.ChatServiceStub(channel)
            request = chat_pb2.ChatQuestionRequest(query=query)
            response = stub.ChatQuestion(request)

            if response.HasField("message"):
                print(f"[✔] response: {response.message}")
                return response.message
            elif response.HasField("error_response"):
                print(f"[✘] error: {response.error_response.code} - {response.error_response.message}")
                return None
            else:
                print("[⚠] empty ChatService")
                return None
    except grpc.RpcError as e:
        print(f"[✘] gRPC error: {e.details()}")
        return None
