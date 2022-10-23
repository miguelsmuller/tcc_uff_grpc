import grpc

from proto import calculations_pb2_grpc
from proto import calculations_pb2

HOST = 'localhost'
PORT = '50051'


def get_roots_equation_by_bhaskara(stub, value_a, value_b, value_c):
    request = calculations_pb2.BhaskaraRequest(value_a=value_a, value_b=value_b, value_c=value_c)

    response = stub.GetRootsEquationByBhaskara(request)

    print(f"The roots of the equation are: ({response.x1}) and ({response.x2})")


def get_fibonacci_sequence(stub, limit, delay):
    request = calculations_pb2.FibonacciSequenceRequest(limit=limit, delay=delay)

    responses = stub.GetFibonacciSequence(request)

    count = 1
    for response in responses:
        print(f"The {count}º fibonacci number: {response.value}")
        count += 1


if __name__ == "__main__":
    with grpc.insecure_channel('{}:{}'.format(HOST, PORT)) as channel:
        stub = calculations_pb2_grpc.CalculationsStub(channel)

        print("-------------- get_roots_equation_by_bhaskara --------------")
        get_roots_equation_by_bhaskara(stub, 1, -1, -12)

        print("-------------- get_fibonacci_sequence --------------")
        get_fibonacci_sequence(stub, 20, 1)
