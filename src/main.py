import asyncio
import json
import logging
import os
import ssl

import websockets

import CloudyCam as cc
import packets
from logger import log

# logging.getLogger('asyncio').setLevel(logging.ERROR)
# logging.getLogger('asyncio.coroutines').setLevel(logging.ERROR)
logging.getLogger('websockets.server').setLevel(logging.ERROR)
logging.getLogger('websockets.protocol').setLevel(logging.ERROR)


def create_camera():
    fp = os.environ.get('CONFIG_FP')
    config = json.load(open(fp, 'rb'))
    cloudycam = cc.CloudyCam(config)
    cloudycam.get_camera()
    return cloudycam

async def send_ping(ws):
    log.info('sending ping')
    pingBuffer = packets.preformat_data(packets.PACKET_TYPES['PING'], bytearray())
    ws.send(pingBuffer)
    ws.ping()

async def consumer_handler(ws, cloudycam):
    i = 0
    while True:
        if i == 200:
            await send_ping(ws)
            i = 0
        message = await ws.recv()
        await packets.process_message(message, cloudycam)
        if len(cloudycam.video_stream) > cloudycam.stream_limit:
            await packets.dump_to_file(cloudycam, ws)
            # log.error(f'Incomplete Read Error {e}...reconnecting')
            # await get_stream_data(cloudycam.stream_host, cloudycam)
        i += 1

async def run(host, cloudycam):
    async with websockets.connect(host) as ws:
        await ws.send(cloudycam.hello_buffer)
        r = await ws.recv()
        formatted_sp_output = await packets.process_message(r, cloudycam)

        await ws.send(formatted_sp_output)
        r = await ws.recv()
        host = await packets.process_message(r, cloudycam)
        return host


async def get_stream_data(stream_host, cloudycam):
    ssl_context = ssl.SSLContext()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with websockets.connect(stream_host, ssl=ssl_context, ping_timeout=None, ping_interval=15, max_queue=2 ** 12) as ws:
        await ws.send(cloudycam.hello_buffer)
        r = await ws.recv()
        formatted_sp_output = await packets.process_message(r, cloudycam)

        await ws.send(formatted_sp_output)
        r = await ws.recv()
        video_id, audio_id = await packets.process_message(r, cloudycam)
        cloudycam.video_channel_id = video_id
        cloudycam.audio_channel_id = audio_id

        await consumer_handler(ws, cloudycam)

async def rerun_on_exception(coro, *args, **kwargs):
    while True:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            log.error(f'Exception: {e}')

if __name__ == '__main__':
    cloudycam = create_camera()
    host = f"wss://{cloudycam.camera['direct_nexustalk_host']}:80/nexustalk"
    stream_host = 'wss://' + asyncio.get_event_loop().run_until_complete(run(host, cloudycam))
    cloudycam.stream_host = stream_host
    loop = asyncio.get_event_loop()
    task = loop.create_task(rerun_on_exception(get_stream_data, stream_host, cloudycam))
    loop.run_forever()

