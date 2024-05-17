import asyncio
import datetime
import logging
import concurrent.futures
import random


class TCPServer(object):
    """TCP server class"""

    def __init__(self, host, port, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._server = asyncio.start_server(self.handle_connection, host=host, port=port)
        self.keepalive_task = None
        self.request_count = 0
        self.clients = []
        self.writers = []

    def start(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        self.keepalive_task = self._loop.create_task(self.keepalive())
        logging.info('Listening established on {0}'.format(self._server.sockets[0].getsockname()))
        if and_loop:
            self._loop.run_forever()

    def stop(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()

    async def keepalive(self):
        while True:
            await asyncio.sleep(5)
            print('Send keepalive')
            for writer in self.writers:
                try:
                    writer.write(f'[{self.request_count}] keepalive\n'.encode(encoding='ascii'))
                    self.request_count += 1
                #   await writer.drain()
                except ConnectionError:
                    if writer in self.writers:
                        self.writers.remove(writer)

    async def handle_connection(self, reader, writer):
        peername = writer.get_extra_info('peername')
        self.clients.append(peername)
        self.writers.append(writer)
        print(f'TCP conntection {peername}')
        while not writer.is_closing():
            try:
                await self.handle_message(reader, writer)
            except concurrent.futures.TimeoutError:
                break
        self.clients.remove(peername)
        if writer in self.writers:
            self.writers.remove(writer)

    async def handle_message(self, reader, writer):
        peername = writer.get_extra_info('peername')

        data = await reader.readline()
        message = data.decode()[0:-1]
        request_time = datetime.datetime.now().strftime('%Y-%m-%d;%H:%M:%S.%f')
        if random.random() > 0.1:
            print(f'Received {message!r} from {peername!r}')
            await asyncio.sleep(random.randint(100, 1000) / 1000)

            client_req_count = message.split(' ')[0][1:-1]
            client_number = self.writers.index(writer) + 1

            async with asyncio.Lock():
                respond_message = f'[{self.request_count}]/{client_req_count} PONG ({client_number})'
                self.request_count += 1
            writer.write((respond_message + '\n').encode(encoding='ascii'))
            await writer.drain()
            response_time = datetime.datetime.now().strftime('%Y-%m-%d;%H:%M:%S.%f')

            print(f'Send message {respond_message} to {peername}')
            logging.info(';'.join([request_time, message, response_time, respond_message]))
        else:
            print(f'Ignored message from {peername}')
            logging.info(';'.join([request_time, message, '(проигнорировано)']))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='server.log', filemode='w')
    server = TCPServer('127.0.0.1', 8888)
    try:
        server.start()
    except KeyboardInterrupt:
        pass  # Press Ctrl+C to stop
    finally:
        server.stop()
