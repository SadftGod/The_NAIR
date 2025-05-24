class Servise_Registrator:
    def __init__(self, server):
        self.server = server

    def register_all(self):
        # defaultRoutes_pb2_grpc.add_DefaultRouterServicer_to_server(
        #     DefaultRouterService(), self.server
        # )
        return self.server