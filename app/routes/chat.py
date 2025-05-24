from app.proto.chat import chat_pb2,chat_pb2_grpc
from modules.decorators.request import not_empty
from modules.decorators.exceptions import RubberCatcher
from modules.palette import Palette as p
from app.validators.defaultValidator import DefaultValidator as dv
from models.requester import Requester as r



class ChatRouter(chat_pb2_grpc.ChatServiceServicer):
    @RubberCatcher(True)
    @not_empty("query")
    async def ChatQuestion(self, request, context):
        query = request.query 
        p.red("Query",query)
        dv.validate_string(query)
        response = r.ask(query)

        return chat_pb2.ChatQuestionResponse(message=response)
        