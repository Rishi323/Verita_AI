import base64
import json
import time
import uuid
import asyncio

from flask import request
from flask_socketio import SocketIO

import numpy as np
import websockets
import os
import dotenv

# Configuration
# load environment variables
dotenv.load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
print(len(OPENAI_API_KEY))
socketio = SocketIO(cors_allowed_origins="*")

url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "OpenAI-Beta": "realtime=v1",
}

active_conversations = {}
processed_audio_chunks = []


# Sockets
def setup_socketio(app):
    socketio.init_app(app)


@socketio.on("connect")
def on_connect():
    sid = request.sid
    print(f"Client connected: {sid}")
    active_conversations[sid] = {"websocket": None}


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    print(f"Client disconnected: {sid}")


@socketio.on("start_conversation")
def start_conversation_wrapper():
    sid = request.sid
    asyncio.run(start_ai_conversation(sid))


@socketio.on("user_audio_chunk")
def on_user_audio_chunk(data):
    sid = request.sid
    print()
    handle_input_audio(sid, data)


@socketio.on("end_audio_input")
def on_end_audio_input():
    sid = request.sid
    if sid not in active_conversations:
        print(f"Error: No active conversation found for session {sid}")
        return

    try:
        time.sleep(0.5)
        asyncio.run(handle_audio_commit(sid))
    except Exception as e:
        print(f"Error handling audio commit for session {sid}: {str(e)}")


###


async def start_ai_conversation(sid):
    print(sid)
    try:
        websocket = await websockets.connect(url, extra_headers=headers)
        active_conversations[sid]["websocket"] = websocket
        await ai_conversation(websocket, sid)

        while True:
            event = await websocket.recv()
            event_data = json.loads(event)
            event_type = event_data.get("type")
            print("EVENT:", event_type)
            handle_event(sid, event_type, event_data)

    except Exception as e:
        print(f"Error in start_conversation for {sid}: {str(e)}")
    finally:
        if sid in active_conversations:
            del active_conversations[sid]


async def ai_conversation(websocket, sid):
    try:
        session_update = {
            "type": "session.update",
            "event_id": f"event_{uuid.uuid4()}",
            "session": {
                "modalities": ["audio", "text"],
                "instructions": "Your knowledge cutoff is 2023-10. You are a helpful assistant.",
                "voice": "alloy",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {"model": "whisper-1"},
                "turn_detection": None,
                "temperature": 0.8,
                "max_response_output_tokens": "inf",
            },
        }

        await send_websocket_event(websocket, session_update)
    except Exception as e:
        print(f"Error in session_update: {str(e)}")

    try:
        conversation_item = {
            "event_id": f"event_{uuid.uuid4()}",
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Hello! My name is John"}],
            },
        }

        await send_websocket_event(websocket, conversation_item)

    except Exception as e:
        print(f"Error in conversation.item.create: {str(e)}")

    try:
        response_create = {
            "event_id": f"event_{uuid.uuid4()}",
            "type": "response.create",
        }

        await send_websocket_event(websocket, response_create)

    except Exception as e:
        print(f"Error in response.create: {str(e)}")

async def send_websocket_event(websocket, event):
    await websocket.send(json.dumps(event))

def extract_event_data(event_data):
    """Extract relevant data from different event types."""
    data = {}
    
    # Handle transcript data
    if 'delta' in event_data and 'text' in event_data['delta']:
        data['transcript'] = event_data['delta']['text']
    
    # Handle response completion data
    if 'response' in event_data:
        output = event_data['response'].get('output', [{}])[0]
        content = output.get('content', [{}])[0]
        data['text'] = content.get('text', '')
    
    return data

def handle_transcript_delta(sid, event_data):
    """Handle incremental transcript updates."""
    if 'delta' in event_data and 'text' in event_data['delta']:
        transcript_text = event_data['delta']['text']
        socketio.emit('transcript_delta', {
            'text': transcript_text
        }, room=sid)
        print(f"Transcript delta: {transcript_text}")

def handle_audio_delta(sid, event_data):
    """Handle audio chunk delivery."""
    try:
        audio_chunk = base64.b64decode(event_data.get("delta", ""))
        # Convert to float32 format
        audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
        audio_float = audio_array.astype(np.float32) / 32768.0
        
        socketio.emit(
            "audio_chunk",
            {"chunk": audio_float.tolist()},  # Convert to list for JSON serialization
            room=sid
        )
    except Exception as e:
        print(f"Error in handle_audio_delta: {str(e)}")
        import traceback
        print(traceback.format_exc())

def handle_response_done(sid, event_data):
    """Handle completion of a response."""
    try:
        final_response = event_data.get('response', {})
        output = final_response.get('output', [{}])[0]
        content = output.get('content', [{}])[0]
        final_text = content.get('text', '')
        
        socketio.emit('response_complete', {
            'text': final_text
        }, room=sid)
        print(f"Response completed: {final_text}")
    except Exception as e:
        print(f"Error in handle_response_done: {str(e)}")

def handle_event(sid, event_type, event_data):
    event_handlers = {
        "session.created": lambda: print("session.created"),
        "session.updated": lambda: print("session.updated", event_data),
        "response.created": lambda: print("response.created"),
        "rate_limits.updated": lambda: print(
            "rate_limits.updated",
            event_data.get("rate_limits", [])[0].get("remaining", "N/A"),
        ),
        "response.audio_transcript.delta": lambda: (
            print("response.audio_transcript.delta"),
        ),
        "response.audio.delta": lambda: handle_audio_delta(sid, event_data),
        "response.audio_transcript.delta": lambda: handle_transcript_delta(sid, event_data),
        "response.audio.done": lambda: print("response.audio.done"),
        "response.audio_transcript.done": lambda: print("response.audio_transcript.done"),
        "response.output_item.done": lambda: print("response.output_item.done"),
        "response.done": lambda: print(
            "response.done",
            event_data.get("response", {})
            .get("output", [{}])[0]
            .get("content", [{}])[0]
            .get("text", ""),
        ),
        "error": lambda: handle_error(event_data),
    }
    handler = event_handlers.get(
        event_type, lambda: print(f"Unhandled event for {event_type}")
    )

    handler()


async def send_websocket_event(websocket, event):
    await websocket.send(json.dumps(event))


def handle_audio_delta(sid, event_data):
    audio_chunk = base64.b64decode(event_data.get("delta", ""))
    # Convert the audio data to float32 format
    audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
    audio_float = audio_array.astype(np.float32) / 32768.0
    
    socketio.emit(
        "audio_chunk",
        {"chunk": audio_float.tobytes()},
        room=sid
    )


def handle_input_audio(sid, data):
    audio_chunk = data.get("audioChunk")
    sample_rate = data.get("sampleRate", 44100)

    print(active_conversations, sid)
    websocket = active_conversations[sid].get("websocket")

    if not websocket:
        print(f"Error: No active WebSocket for session {sid}")
        return

    if audio_chunk:
        try:
            if isinstance(audio_chunk, str):
                audio_bytes = base64.b64decode(audio_chunk)
            elif isinstance(audio_chunk, bytes):
                audio_bytes = audio_chunk
            else:
                raise ValueError(f"Unsupported audio_chunk format: {type(audio_chunk)}")

            print(f"Audio chunk length: {len(audio_bytes)} bytes")
            print(f"Sample rate: {sample_rate}")

            if len(audio_bytes) % 2 != 0:
                audio_bytes = audio_bytes[:-1]

            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)

            audio_float = audio_array.astype(np.float32) / 32768.0

            base64_chunk = base64.b64encode(audio_float.tobytes()).decode("utf-8")

            processed_audio_chunks.append({"audio": base64_chunk})

            print(
                f"Processed audio chunk for session {sid}, length: {len(audio_float)} samples, sample_rate: {sample_rate}"
            )
        except Exception as e:
            print(
                f"Error processing and sending audio chunk for session {sid}: {str(e)}"
            )
            import traceback

            print(traceback.format_exc())
    else:
        print(f"Invalid audio data received for session {sid}")


async def handle_audio_commit(sid):
    websocket = active_conversations[sid].get("websocket")
    if not websocket:
        print(f"Error: No active WebSocket for session {sid}")
        return

    try:
        for chunk in processed_audio_chunks:
            print(type(chunk["audio"]))
            input_audio_buffer_append = {
                "event_id": f"event_{uuid.uuid4()}",
                "type": "input_audio_buffer.append",
                "audio": chunk["audio"],
            }
            await send_websocket_event(websocket, input_audio_buffer_append)

        input_audio_buffer_commit = {
            "event_id": f"event_{uuid.uuid4()}",
            "type": "input_audio_buffer.commit",
        }
        await send_websocket_event(websocket, input_audio_buffer_commit)

        print(f"Successfully appended audio buffer for session {sid}")
    except Exception as e:
        print(f"Error appending or committing audio buffer for session {sid}: {str(e)}")
        import traceback

        print(traceback.format_exc())

    try:
        response_create = {
            "event_id": f"event_{uuid.uuid4()}",
            "type": "response.create",
        }
        await send_websocket_event(websocket, response_create)
    except Exception as e:
        print(f"Error committing audio buffer for session {sid}: {str(e)}")


def handle_error(error_data):
    error = error_data.get("error", {})
    print(
        f"Error occurred: Type: {error.get('type')}, Code: {error.get('code')}, Message: {error.get('message')}"
    )

@socketio.on_error()
def error_handler(e):
    print(f"SocketIO error: {str(e)}")
