import asyncio
import json
import os
from dotenv import load_dotenv
import websockets
from .voice_agent_config.settings import SETTINGS
from .audio_player import AudioPlayer
from .audio_manager import AudioManager
from .config import settings
from .voice_agent_config.smart_home_controller import control_smart_home

load_dotenv()
DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY")

class VoiceAgent:
    def __init__(self):
        self.connection = None
        self.url = "wss://agent.deepgram.com/v1/agent/converse"
        self._audio_player = None
        self._audio_manager = AudioManager()
        self._mic_stream = None
        self._is_running = False

    async def listen(self, inactivity_timeout: int = 10):
        """
        Establishes a websocket connection to Deepgram Agent API,
        sends microphone audio, and processes incoming responses.
        
        Args:
            inactivity_timeout: Seconds of inactivity before closing connection (default: 10)
        """
        self._is_running = True
        self._inactivity_timeout = inactivity_timeout
        
        try:
            headers = {
                "Authorization": f"Token {DEEPGRAM_API_KEY}"
            }
            
            async with websockets.connect(self.url, additional_headers=headers) as websocket:
                self.connection = websocket
                print(f"🔌 Connected to Deepgram Agent API (inactivity timeout: {inactivity_timeout}s)")
                
                # Start the audio player for playback
                self._audio_player = AudioPlayer()
                self._audio_player.start()
                
                # Set up microphone input stream
                device_index = self._audio_manager.get_device_index()
                detected_rate = self._audio_manager.get_device_sample_rate(device_index)
                self._mic_stream = self._audio_manager.open_input_stream(
                    device_index=device_index,
                    rate=detected_rate,
                    chunk_size=settings.audio_chunk_size,
                    channels=settings.audio_channels
                )
                print(f"🎤 Microphone stream opened (rate: {detected_rate}Hz)")
                
                # Run send and receive tasks concurrently
                await asyncio.gather(
                    self._send_audio_task(),
                    self._receive_messages_task()
                )

        except Exception as e:
            print(f"Error in listen: {e}")
            raise
        finally:
            self._is_running = False
            # Clean up microphone stream
            if self._mic_stream:
                self._audio_manager.close_stream(self._mic_stream)
                self._mic_stream = None
            # Stop audio player
            if self._audio_player:
                self._audio_player.stop()
                self._audio_player = None
            print("✅ Voice session ended")

    async def _send_audio_task(self):
        """
        Continuously captures audio from microphone and sends to websocket.
        Runs in a loop until _is_running is False.
        """
        print("📤 Starting audio send task...")
        
        while self._is_running and self.connection:
            try:
                # Read audio chunk from microphone (blocking, so use thread)
                audio_data = await asyncio.to_thread(
                    self._mic_stream.read,
                    settings.audio_chunk_size,
                    exception_on_overflow=False
                )
                
                # Send raw audio bytes to Deepgram
                await self.connection.send(audio_data)
                
            except websockets.exceptions.ConnectionClosed:
                print("📤 Send task: connection closed")
                break
            except Exception as e:
                print(f"📤 Send task error: {e}")
                break
    
    async def _receive_messages_task(self):
        """
        Receives and processes messages from the websocket.
        Runs in a loop until _is_running is False.
        Closes connection if no messages received within inactivity_timeout.
        """
        print("📥 Starting message receive task...")
        
        while self._is_running and self.connection:
            try:
                # Receive message from websocket with inactivity timeout
                message = await asyncio.wait_for(
                    self.connection.recv(),
                    timeout=self._inactivity_timeout
                )
                
                # Handle different message types
                if isinstance(message, bytes):
                    # Binary message (audio data) - play through speaker
                    if self._audio_player:
                        self._audio_player.play(message)
                elif isinstance(message, str):
                    # Text message - try to parse as JSON
                    try:
                        parsed = json.loads(message)
                        await self._handle_json_message(parsed)
                    except json.JSONDecodeError:
                        # Plain text message
                        print(f"📝 Text message received: {message}")
                else:
                    # Unknown message type
                    print(f"❓ Unknown message type: {type(message)}")
                    print(f"   Content: {message}")
            
            except asyncio.TimeoutError:
                print(f"⏱️  No messages received for {self._inactivity_timeout}s, closing connection")
                self._is_running = False
                break
            except websockets.exceptions.ConnectionClosed:
                print("📥 Receive task: connection closed")
                break
            except Exception as e:
                print(f"📥 Receive task error: {e}")
                break
    
    async def _handle_json_message(self, parsed: dict):
        """Handle parsed JSON messages from Deepgram."""
        msg_type = parsed.get("type", "unknown")
        
        if msg_type == "Welcome":
            print("👋 Welcome message received, sending SETTINGS...")
            asyncio.create_task(self._send_settings())
        elif msg_type == "SettingsApplied":
            print("✅ Settings applied successfully")
        elif msg_type == "UserStartedSpeaking":
            print("🗣️  User started speaking")
            # Interrupt agent audio immediately
            if self._audio_player:
                self._audio_player.clear()
        elif msg_type == "AgentStartedSpeaking":
            print("🤖 Agent started speaking")
        elif msg_type == "ConversationText":
            role = parsed.get("role", "unknown")
            content = parsed.get("content", "")
            print(f"💬 [{role}]: {content}")
        elif msg_type == "AgentAudioDone":
            print("🤖 Agent finished speaking")
        elif msg_type == "AgentThinking":
            print("🤖 Agent is thinking here are it's thoughts:")
            print("💭 " + parsed.get("content", ""))
            asyncio.create_task(self._inject_agent_message())
        elif msg_type == "FunctionCallRequest":
            functions = parsed.get("functions", [])
            if len(functions) > 1:
                raise NotImplementedError(
                    "Multiple functions not supported"
                )
            function_name = functions[0].get("name")
            function_call_id = functions[0].get("id")
            parameters = json.loads(functions[0].get("arguments", {}))
            await control_smart_home(parameters)
            function_call_response = {
                "type": "FunctionCallResponse",
                "name": function_name,
                "id": function_call_id,
                "content": "The function call was successful."
            }
            asyncio.create_task(self._send_function_call_response(function_call_response))
        else:
            # Log other message types
            print(f"📨 {msg_type}: {json.dumps(parsed, indent=2)}")
    
    async def _send_settings(self):
        """Send settings configuration to Deepgram."""
        if self.connection:
            await self.connection.send(json.dumps(SETTINGS))
            print("✅ SETTINGS sent successfully")

    # I've built this but it doesn't come up very often in my testing. I just wanted to account for it.
    async def _inject_agent_message(self):
        """Inject agent message while agent is thinking."""
        inject_message = {
            "type": "InjectAgentMessage",
            "message": "Hang on just a minute."
        }
        if self.connection:
            await self.connection.send(json.dumps(inject_message))
            print("✅ Inject Agent Message sent successfully")

    async def _send_function_call_response(self, function_call_response):
        """Send FunctionCallResponse to Deepgram."""
        if self.connection:
            await self.connection.send(json.dumps(function_call_response))
            print("✅ Function Call Response sent successfully")

    async def close(self):
        """Close the connection"""
        if self.connection:
            await self.connection.close()
