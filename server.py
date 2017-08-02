from concurrent import futures
import time
import random


import grpc

import testing_pb2
import testing_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
random.seed()

class Tester(testing_pb2_grpc.TesterServicer):
  def Predict(self, request, context):
    time.sleep(5)
    print('Hello, %s!' % request.id)
    return testing_pb2.PredictReply(result='Hello, %s!' % request.id)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  testing_pb2_grpc.add_TesterServicer_to_server(Tester(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()