import asyncio
import json
import os
import time
from dotenv import load_dotenv
import websockets
from .voice_agent_config.settings import SETTINGS
# from backend.config import DEEPGRAM_API_KEY

load_dotenv()
DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY")

class VoiceAgent:
    def __init__(self):
        self.connection = None
        self.url = "wss://agent.deepgram.com/v1/agent/converse"

    async def listen(self, timeout_seconds: int = 5):
        """
        Establishes a websocket connection to Deepgram Agent API
        and processes incoming data for a specified duration.
        
        Args:
            timeout_seconds: Duration in seconds to listen before closing (default: 5)
        """
        start_time = time.time()
        
        try:
            headers = {
                "Authorization": f"Token {DEEPGRAM_API_KEY}"
            }
            
            async with websockets.connect(self.url, additional_headers=headers) as websocket:
                self.connection = websocket
                print(f"🔌 Connected to Deepgram Agent API (listening for {timeout_seconds}s)")
                
                # Listen for all incoming messages from the websocket
                while True:
                    # Check if timeout has been reached
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= timeout_seconds:
                        print(f"⏱️  {timeout_seconds}s timeout reached, closing connection")
                        break
                    
                    try:
                        # Receive and handle all incoming messages
                        message = await asyncio.wait_for(
                            self.connection.recv(),
                            timeout=0.1
                        )
                        
                        # Handle different message types
                        if isinstance(message, bytes):
                            # Binary message (audio data)
                            print(f"📦 Binary message received: {len(message)} bytes")
                            print(f"   First 50 bytes: {message[:50]}")
                        elif isinstance(message, str):
                            # Text message - try to parse as JSON
                            try:
                                parsed = json.loads(message)
                                print(f"📨 JSON message received:")
                                print(f"   {json.dumps(parsed, indent=2)}")
                                
                                # Handle Welcome message - send SETTINGS
                                if parsed.get("type") == "Welcome":
                                    print("👋 Welcome message received, sending SETTINGS...")
                                    await self.connection.send(json.dumps(SETTINGS))
                                    print("✅ SETTINGS sent successfully")
                                    
                            except json.JSONDecodeError:
                                # Plain text message
                                print(f"📝 Text message received: {message}")
                        else:
                            # Unknown message type
                            print(f"❓ Unknown message type: {type(message)}")
                            print(f"   Content: {message}")
                    
                    except asyncio.TimeoutError:
                        # No message received within timeout, continue loop
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        print("🔌 Websocket connection closed by server")
                        break
                    except Exception as e:
                        print(f"❌ Error receiving message: {e}")
                        break

        except Exception as e:
            print(f"Error in listen: {e}")
            raise
        finally:
            print("✅ Voice session ended")

    async def close(self):
        """Close the connection"""
        if self.connection:
            await self.connection.close()
