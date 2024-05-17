import asyncio
import datetime
import logging
import random
import sys


class EchoClient(object):
    def __init__(self, name):
        self.request_count = 0
        self.name = name

    async def tcp_echo_client(self, message):
        logging.basicConfig(level=logging.INFO, filename=f'client_{self.name}.log', filemode='w')
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)
        while not writer.is_closing():
            await asyncio.sleep(random.randint(300, 3000) / 1000)
            req_message = f'[{self.request_count}] {message}'
            writer.write((req_message + '\n').encode(encoding='ascii'))
            await writer.drain()
            request_time = datetime.datetime.now().strftime('%Y-%m-%d;%H:%M:%S.%f')

            print(f'Send message {req_message}')
            self.request_count += 1

            try:
                data = await asyncio.wait_for(reader.read(100), 4)
                for respond_message in data.decode().split('\n'):
                    if not respond_message:
                        break
                    if 'keepalive' in respond_message:
                        logging.info('keepalive')
                    else:
                        respond_time = datetime.datetime.now().strftime('%Y-%m-%d;%H:%M:%S.%f')
                        logging.info(';'.join([request_time, req_message, respond_time, respond_message]))
                    print('raw data received: {}'.format(respond_message))
            except:
                logging.info(
                    ';'.join([request_time,
                              req_message,
                              datetime.datetime.now().strftime('%Y-%m-%d;%H:%M:%S.%f'),
                              '(таймаут)']))
                print('Timeout!')
                writer.close()

        print('Close the connection')
        writer.close()
        await writer.wait_closed()


async def start_echo_client(name):
    c = EchoClient(name)
    await c.tcp_echo_client('PING')


if __name__ == '__main__':
    asyncio.run(start_echo_client(sys.argv[1]))
