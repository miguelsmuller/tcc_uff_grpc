from concurrent import futures
import time
import grpc

from proto import calcs_pb2_grpc
from proto import calcs_pb2


class LocalCalcsServicer(calcs_pb2_grpc.CalcsServicer):

    def GetBhaskara(self, request, context):
        print("\n=== server bhaskara")

        a, b, c = request.var_a, request.var_b, request.var_c

        delta = (b ** 2) - 4 * a * c

        if a == 0:
            value1 = value2 = 0
        elif delta < 0:
            value1 = value2 = 0
        else:
            value1 = (-b + delta ** (1 / 2)) / (2 * a)
            value2 = (-b - delta ** (1 / 2)) / (2 * a)

        print(f"server roots: ({value1}) and ({value2})")
        return calcs_pb2.RootsReply(x1=value1, x2=value2)

    def GetFibonacci(self, request, context):
        print("\n=== server fibonacci")

        # metadata = context.invocation_metadata()
        # metadata_dict = {}
        # for c in metadata:
        #     metadata_dict[c.key] = c.value
        # print(metadata_dict)

        if request.limit == 0:
            print(f"1º server fibonacci number: 0")
            yield calcs_pb2.FibonacciReply(value=0)

        elif request.limit >= 1:
            a, b = 0, 1
            print(f"1º server fibonacci number: {a} - {time.time()}")
            yield calcs_pb2.FibonacciReply(value=a)
            time.sleep(request.delay)

            for count in range(request.limit):
                a, b = b, a + b
                print(f"{count+2}º server fibonacci number: {a} - {time.time()}")
                yield calcs_pb2.FibonacciReply(value=a)
                time.sleep(request.delay)


def start_local_serve():
    local_server = grpc.server(futures.ThreadPoolExecutor())

    calcs_pb2_grpc.add_CalcsServicer_to_server(LocalCalcsServicer(), local_server)

    local_server.add_insecure_port('[::]:' + '50051')
    local_server.start()

    print("Server started, listening on " + '50051')

    local_server.wait_for_termination()


if __name__ == '__main__':
    start_local_serve()
