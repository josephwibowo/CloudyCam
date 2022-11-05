import asyncio
import io
import datetime
import os
import random
import time
import ssl
from subprocess import Popen, check_output
from subprocess import Popen, PIPE
import threading

import sys

import websocket

from logger import log

import proto.Redirect_pb2 as red
import proto.StartPlayback_pb2 as sp
import proto.Playback_pb2 as pb
import proto.PlaybackBegin_pb2 as pbb

PACKET_TYPES = {
    'PING': 1,
    'HELLO': 100,
    'PING_CAMERA': 101,
    'AUDIO_PAYLOAD': 102,
    'START_PLAYBACK': 103,
    'STOP_PLAYBACK': 104,
    'CLOCK_SYNC_ECHO': 105,
    'LATENCY_MEASURE': 106,
    'TALKBACK_LATENCY': 107,
    'METADATA_REQUEST': 108,
    'OK': 200,
    'ERROR': 201,
    'PLAYBACK_BEGIN': 202,
    'PLAYBACK_END': 203,
    'PLAYBACK_PACKET': 204,
    'LONG_PLAYBACK_PACKET': 205,
    'CLOCK_SYNC': 206,
    'REDIRECT': 207,
    'TALKBACK_BEGIN': 208,
    'TALKBACK_END': 209,
    'METADATA': 210,
    'METADATA_ERROR': 211,
    'AUTHORIZE_REQUEST': 212
}
PACKET_INV = {v: k for k, v in PACKET_TYPES.items()}

PROFILES = {
    'AUDIO_AAC': 3,
    'AUDIO_SPEEX': 4,
    'AUDIO_OPUS': 5,
    'AUDIO_OPUS_LIVE': 13,
    'VIDEO_H264_50KBIT_L12': 6,
    'VIDEO_H264_530KBIT_L31': 7,
    'VIDEO_H264_100KBIT_L30': 8,
    'VIDEO_H264_2MBIT_L40': 9,
    'VIDEO_H264_50KBIT_L12_THUMBNAIL': 10,
    'META': 11,
    'DIRECTORS_CUT': 12,
    'VIDEO_H264_L31': 14,
    'VIDEO_H264_L40': 15,
    'AVPROFILE_MOBILE_1': 1,
    'AVPROFILE_HD_MAIN_1': 2
}
CODECS = {
    "SPEEX": 0,
    "PCM_S16_LE": 1,
    "H264": 2,
    "AAC": 3,
    "OPUS": 4,
    "META": 5,
    "DIRECTORS_CUT": 6
}

def find_int_byte_size(x):
    return (x.bit_length()+7) // 8





async def send_inf_ping(ws):
    while True:
        log.info('sending inf ping')
        pingBuffer = preformat_data(PACKET_TYPES['PING'], bytearray())
        ws.send(pingBuffer, websocket.ABNF.OPCODE_BINARY)
        time.sleep(30)

async def process_message(byte_string, cloudycam):
    buffer = bytearray(byte_string)
    packet_type = buffer[0]
    header_length = 3

    if packet_type == PACKET_TYPES.get('LONG_PLAYBACK_PACKET'):
        header_length = 5

    payload = buffer[header_length:]
    return handle_packet_data(packet_type, payload, cloudycam)

def on_error(wsapp, err):
  log.error(f"Got an error: {err}, url was {wsapp.url}")

def handle_packet_data(packet_type, payload, cloudycam):
    if packet_type == PACKET_TYPES['OK']:
        log.info('OK packet received. Starting playback...')
        formatted_sp_output = start_playback(cloudycam.camera)
        return formatted_sp_output
        # ws.send(formatted_sp_output, websocket.ABNF.OPCODE_BINARY)
    elif packet_type == PACKET_TYPES['REDIRECT']:
        log.info('Redirect packet received. Redirecting...')
        # ws.close()
        redirect = red.Redirect().FromString(payload)
        cloudycam.stream_host = redirect.NewHost
        return redirect.NewHost
        # setup_connection(redirect.NewHost, cloudycam, cloudycam.hello_buffer, True)
    elif packet_type == PACKET_TYPES['PLAYBACK_BEGIN']:
        return handle_playback_begin(payload)
    elif packet_type in [PACKET_TYPES['PLAYBACK_PACKET'], PACKET_TYPES['LONG_PLAYBACK_PACKET']]:
        handle_playback(payload, cloudycam, packet_type)
    elif packet_type == PACKET_TYPES['PING']:
        log.info('PING received.')
    else:
        log.info(f'Packet received: {packet_type}, {PACKET_INV[packet_type]}')

def handle_playback_begin(payload):
    log.info('Playback begin packet received.')
    b = pbb.PlaybackBegin().FromString(payload)
    video_channel_id, audio_channel_id = None, None
    for ch in b.Channels:
        if ch.CodecType == CODECS['H264']:
            video_channel_id = ch.ChannelId
        elif ch.CodecType == CODECS['AAC']:
            audio_channel_id = ch.ChannelId
    return video_channel_id, audio_channel_id


def handle_playback(payload, cloudycam, packet_type):
    # log.info(f'{PACKET_INV[packet_type]} packet received.')
    b = pb.Playback().FromString(payload)
    if b.ChannelId == cloudycam.video_channel_id:
        h264_header = bytearray([0x00, 0x00, 0x00, 0x01])
        payload_bytes = bytearray()
        for x in list(b.Payload):
            payload_bytes.extend(x)
        h264_header.extend(payload_bytes)
        cloudycam.video_stream.append(h264_header)
        # log.info(f"Video payload length: {len(h264_header)} Bitrate: {b.TimestampDelta} Video cache length: {len(cloudycam.video_stream)}")
    elif b.ChannelId == cloudycam.audio_channel_id:
        cloudycam.audio_stream.extend(b.Payload)
        # log.info(f"Audio payload length: {len(b.Payload)} Bitrate: {b.TimestampDelta} Audio cache length: {len(cloudycam.audio_stream)}")


def preformat_data(packet_type, buffer):
    if packet_type == PACKET_TYPES.get('LONG_PLAYBACK_PACKET'):
        request_buffer = [0, 0, 0, 0, 0]
    else:
        request_buffer = [0, 0, 0]
    request_buffer[0] = packet_type

    buffer_length = len(buffer)
    byte_data = bytearray(buffer_length.to_bytes(find_int_byte_size(buffer_length), 'big'))

    if len(byte_data) == 1:
        request_buffer[-1:] = byte_data
    else:
        request_buffer[1:] = byte_data
    request_buffer.extend(buffer)
    final_buffer = bytearray(request_buffer)
    return final_buffer


def start_playback(camera_info):
    other_profiles = []
    for c in camera_info['capabilities']:
        if 'streaming.cameraprofile' in c:
            profile = c.split('.')[-1]
            if PROFILES.get(profile):
                other_profiles.append(PROFILES[profile])
    if camera_info['properties']['audio.enabled']:
        other_profiles.append(PROFILES['AUDIO_AAC'])

    #startplayback model
    playback_container = sp.StartPlayback()
    playback_container.SessionId = random.randint(0,100)
    playback_container.Profile = PROFILES['VIDEO_H264_2MBIT_L40']
    playback_container.OtherProfiles.extend(other_profiles)

    sp_buffer = bytearray(io.BytesIO(playback_container.SerializeToString()).getvalue())
    formatted_sp_output = preformat_data(PACKET_TYPES['START_PLAYBACK'], sp_buffer)
    return formatted_sp_output


async def send_ping(ws):
    log.info('sending ping')
    pingBuffer = preformat_data(PACKET_TYPES['PING'], bytearray())
    await ws.send(pingBuffer)
    await ws.ping()


async def dump_to_file(cloudycam, ws):
    fn = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S") + ".mp4"
    log.info(f'Dumping file to {fn}')
    args = [
        cloudycam.config['ffmpeg_path'],
        '-f', 'h264',
        '-loglevel', 'fatal',
        '-i', 'pipe:',
        '-vsync', 'vfr',
        '-bf', '0',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-an',
        fn
    ]
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
    video = b''.join(cloudycam.video_stream)
    out, err = p.communicate(video)
    log.info(out)
    log.info(err)


    args = [
        cloudycam.config['ffmpeg_path'],
        '-i', fn,
        '-i', 'pipe:',
        'videos/' + fn
    ]
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
    audio = b''.join(cloudycam.audio_stream)
    p.communicate(audio)

    cloudycam.video_stream = []
    cloudycam.audio_stream = []
    os.remove(fn)

