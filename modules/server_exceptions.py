try:
   import ast  
   import traceback        
   from grpc import StatusCode
   from modules.palette import Palette as p
except Exception as e:
   p.yellowFatTag("Exception Error",f"Can not import modules {e}")
   pass

class RubberException(Exception):
    def __init__(self, error:str, status:int) -> dict:
        super().__init__({"error": {error}, "status": {status}})
        self.error = error 
        self.status = status
             
    def raiseRubber(self):
        
        raise self
    
    def detail():
        traceback.print_exc()
        
    def ErrorPlater(error:str,status:int,context):
        
        STATUS_CODE_MAP = {
            0: StatusCode.OK,
            1: StatusCode.CANCELLED,
            2: StatusCode.UNKNOWN,
            3: StatusCode.INVALID_ARGUMENT,
            4: StatusCode.DEADLINE_EXCEEDED,
            5: StatusCode.NOT_FOUND,
            6: StatusCode.ALREADY_EXISTS,
            7: StatusCode.PERMISSION_DENIED,
            8: StatusCode.RESOURCE_EXHAUSTED,
            9: StatusCode.FAILED_PRECONDITION,
            10: StatusCode.ABORTED,
            11: StatusCode.OUT_OF_RANGE,
            12: StatusCode.UNIMPLEMENTED,
            13: StatusCode.INTERNAL,
            14: StatusCode.UNAVAILABLE,
            15: StatusCode.DATA_LOSS,
            16: StatusCode.UNAUTHENTICATED,
        }
        grpc_code = STATUS_CODE_MAP.get(status, StatusCode.UNKNOWN)

        context.set_code(grpc_code)
        context.set_details(error)

        
        return error

   
        
    def catcher(e:Exception,context):
        if isinstance(e, RubberException):
            errorExc = ast.literal_eval(str(e))
            
            error = list(errorExc["error"])[0]
            status = list(errorExc['status'])[0]
            
            if status == 0 and str(status) == "0":
                return RubberException.PositivePlate(error,status,context)

            if status:
                return RubberException.ErrorPlater(str(error),status,context)
        elif isinstance(e,FileNotFoundError):
            return RubberException.ErrorPlater(str(e),500,context)
        return RubberException.ErrorPlater(str(e),500,context)
        
    
    def fastRubber(error,status):
        re = RubberException(error,status)
        re.raiseRubber()
        
        
    @staticmethod
    def dbRubber(exception):
        RubberException.fastRubber(f"Can not connect to database : {exception}",15)

    @staticmethod
    def notFind():
        RubberException.fastRubber(f"Content not founded",5)
        
    @staticmethod
    def unknow(e):
        RubberException.fastRubber(f"Something gone wrong: {e}",2)
        
    @staticmethod
    def positive(text:str,user,status):
        combine = {"message":text,"user":user}
        if status != 0:
            RubberException.fastRubber("Wrong usage of Positive returner",13)
        RubberException.fastRubber(str(combine),status)
        
    @staticmethod
    def positive_token(token:str,user):
        status = 0
        if user is None:
                RubberException.fastRubber("User must be provided for gRPC positive_token", 5)
        RubberException.positive(token,user,status)
  