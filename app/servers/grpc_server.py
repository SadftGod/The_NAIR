from concurrent import futures
import grpc
from app.services.grpc_registrator import Servise_Registrator
from grpc_reflection.v1alpha import reflection

class GRPC_server:
    def __call__(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        sr = Servise_Registrator(server)
        server = sr.register_all()
        
        service_names = []
        for handler in server._state.generic_handlers:
            if hasattr(handler, 'service_name') and callable(handler.service_name):
                service_names.append(handler.service_name())
        service_names.append(reflection.SERVICE_NAME)


        reflection.enable_server_reflection(service_names, server)

        return server