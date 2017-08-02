import asyncio
from aio_pika import connect, IncomingMessage
import grpc
import testing_pb2
import testing_pb2_grpc
import os
import sys
import logging

def _fwrap(f, gf):
    logging.info("IN HERE")
    try:
        f.set_result(gf.result())
    except Exception as e:
        f.set_exception(e)

def fwrap(gf, loop=None):
    '''
        Wraps a GRPC result in a future that can be yielded by asyncio
        
        Usage::
        
            async def my_fn(param):
                result = await fwrap(stub.function_name.future(param, timeout))
        
    '''
    f = asyncio.Future()

    if loop is None:
        loop = asyncio.get_event_loop()

    # gf.add_done_callback(lambda _: loop.call_soon(_fwrap, f, gf))
    gf.add_done_callback(lambda _: loop.call_soon_threadsafe(_fwrap, f, gf))
    return f

async def on_message(message: IncomingMessage):
    with message.process():

        # make three grpc calls
        logging.info("Predict client 1 %s sent request" % message.body)
        f1 = doGRPC(message.body, 1)
        logging.info("Predict client 2 %s sent request" % message.body)
        f2 = doGRPC(message.body, 2)
        logging.info("Predict client 3 %s sent request" % message.body)
        f3 = doGRPC(message.body, 3)
        # wait until they are all done, then continue
        logging.info("Waiting...")
        # time.sleep(55)
        await asyncio.wait([f1, f2, f3])
        logging.info("Done Waiting...")

def doGRPC(id, server_id):
    stub = testing_pb2_grpc.TesterStub(grpc_channel)
    response_future = stub.Predict.future(testing_pb2.PredictRequest(id=id))
    response_future.add_done_callback(_create_rpc_callback(server_id))
    return fwrap(response_future)

def _create_rpc_callback(server_id):
    def _callback(response_future):
        exception = response_future.exception()
        if exception:
          logging.error(exception)
        else:
          logging.info("Server " + str(server_id) + " sent: " + response_future.result().result)
    return _callback


async def main():
    logging.info(os.getpid())

    global grpc_channel
    grpc_channel = grpc.insecure_channel('localhost:50051')

    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/", loop=loop)

    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declaring queue
    queue = await channel.declare_queue('task_queue', durable=True)

    # Start listening the queue with name 'task_queue'
    queue.consume(on_message)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    loop = asyncio.get_event_loop()
    loop.create_task(main())

    # we enter a never-ending loop that waits for data and runs
    # callbacks whenever necessary.
    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()