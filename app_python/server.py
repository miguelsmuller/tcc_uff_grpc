from concurrent import futures
import time
import grpc

from proto import calculations_pb2_grpc
from proto import calculations_pb2

PORT = '50051'


class CalculationsServicer(calculations_pb2_grpc.CalculationsServicer):

    def GetRootsEquationByBhaskara(self, request, context, *args, **kwargs):
        a = request.value_a
        b = request.value_b
        c = request.value_c

        delta = (b ** 2) - 4 * a * c

        if a == 0:
            value1 = value2 = 0
        elif delta < 0:
            value1 = value2 = 0
        else:
            value1 = (-b + delta ** (1 / 2)) / (2 * a)
            value2 = (-b - delta ** (1 / 2)) / (2 * a)

        response = calculations_pb2.RootsEquationReply(x1=value1, x2=value2)
        return response

    def GetFibonacciSequence(self, request, context, *args, **kwargs):
        for response in range(request.limit):

            response = calculations_pb2.FibonacciSequenceReply(value=response)
            time.sleep(request.delay)
            yield response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    calculations_pb2_grpc.add_CalculationsServicer_to_server(CalculationsServicer(), server)

    server.add_insecure_port('[::]:' + PORT)
    server.start()

    print("Server started, listening on " + PORT)

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
