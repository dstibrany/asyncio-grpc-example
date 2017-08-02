import sys
import asyncio
from aio_pika import connect, Message, DeliveryMode


async def main(loop):
    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/", loop=loop)

    # Creating a channel
    channel = await connection.channel()


    # Sending the message
    for i in range(1, 1000):
        message = Message(
            bytes(str(i).encode('utf-8')),
            delivery_mode=DeliveryMode.PERSISTENT
        )
        await channel.default_exchange.publish(
            message, routing_key='task_queue'
        )

        print(" [x] Sent %r" % message)

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))