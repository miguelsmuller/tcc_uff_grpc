import grpc
import time
from proto import calcs_pb2_grpc
from proto import calcs_pb2

HOST = 'localhost'
PORT = '50051'


def get_bhaskara(stub, a, b, c):
    request = calcs_pb2.BhaskaraRequest(var_a=a, var_b=b, var_c=c)
    response = stub.GetBhaskara(request)
    print(f"client roots: ({response.x1}) and ({response.x2})")


def get_fibonacci(stub, limit, delay):
    # timeout_seconds = 999
    # metadata = [(b'key1', b'value1'), (b'key2', b'value2')]
    # request = calcs_pb2.FibonacciRequest(limit=limit, delay=delay)
    # responses = stub.GetFibonacci(request, timeout_seconds, metadata=metadata)

    request = calcs_pb2.FibonacciRequest(limit=limit, delay=delay)
    responses = stub.GetFibonacci(request)
    count = 1
    for response in responses:
        print(f"{count}º client fibonacci number: {response.value} - {time.time()}")
        count += 1


if __name__ == "__main__":
    with grpc.insecure_channel('{}:{}'.format(HOST, PORT)) as channel:
        stub = calcs_pb2_grpc.CalcsStub(channel)

        print("\n=== client bhaskara")
        a = 1
        b = -1
        c = -12
        get_bhaskara(stub, a, b, c)

        print("\n=== client fibonacci")
        limit = 8
        delay = 1
        get_fibonacci(stub, limit, delay)
