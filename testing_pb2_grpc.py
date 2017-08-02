# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import testing_pb2 as testing__pb2


class TesterStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Predict = channel.unary_unary(
        '/testgrpc.Tester/Predict',
        request_serializer=testing__pb2.PredictRequest.SerializeToString,
        response_deserializer=testing__pb2.PredictReply.FromString,
        )


class TesterServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Predict(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TesterServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Predict': grpc.unary_unary_rpc_method_handler(
          servicer.Predict,
          request_deserializer=testing__pb2.PredictRequest.FromString,
          response_serializer=testing__pb2.PredictReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'testgrpc.Tester', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))