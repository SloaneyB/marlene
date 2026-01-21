"""FastAPI server for Marlene smart home assistant."""
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
from backend.config import settings
from backend.wake_word_detector import WakeWordDetector
from backend.voice_agent import VoiceAgent

logger = logging.getLogger(__name__)


app = FastAPI(title="Marlene Smart Home Assistant", version="0.1.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
wake_word_detector: Optional[WakeWordDetector] = None
voice_agent: Optional[VoiceAgent] = None
status = {
    "listening": False,
    "processing": False,
    "last_command": None,
    "last_transcript": None
}


class CommandRequest(BaseModel):
    """Request model for manual voice commands."""
    duration: int = 5


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Marlene Smart Home Assistant",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/status")
async def get_status():
    """Get current system status."""
    return JSONResponse(status)


@app.post("/start-listening")
async def start_listening():
    """Start wake word detection."""
    global wake_word_detector
    
    if status["listening"]:
        return JSONResponse({"message": "Already listening"}, status_code=400)
    
    try:
        def on_wake_word_detected():
            """Callback when wake word is detected."""
            status["processing"] = True
            # Trigger voice command processing
            voice_agent.process_voice_command_sync(duration_seconds=5)
            status["processing"] = False
        
        wake_word_detector = WakeWordDetector(on_wake_word=on_wake_word_detected)
        
        # Start in background
        asyncio.create_task(asyncio.to_thread(wake_word_detector.start))
        status["listening"] = True
        
        return JSONResponse({"message": "Wake word detection started"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/stop-listening")
async def stop_listening():
    """Stop wake word detection."""
    global wake_word_detector
    
    if not status["listening"]:
        return JSONResponse({"message": "Not currently listening"}, status_code=400)
    
    if wake_word_detector:
        wake_word_detector.stop()
        wake_word_detector = None
    
    status["listening"] = False
    return JSONResponse({"message": "Wake word detection stopped"})


@app.post("/process-command")
async def process_command(request: CommandRequest):
    """Manually trigger voice command processing."""
    if status["processing"]:
        return JSONResponse({"message": "Already processing a command"}, status_code=400)
    
    try:
        status["processing"] = True
        await voice_agent.process_voice_command(duration_seconds=request.duration)
        status["processing"] = False
        
        return JSONResponse({"message": "Command processed successfully"})
    except Exception as e:
        status["processing"] = False
        return JSONResponse({"error": str(e)}, status_code=500)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    
    try:
        while True:
            # Send status updates every second
            await websocket.send_json(status)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    global voice_agent
    voice_agent = VoiceAgent()
    logger.info(f"Marlene API Server starting on {settings.api_host}:{settings.api_port}")
    logger.info(f"API Docs: http://{settings.api_host}:{settings.api_port}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global wake_word_detector, voice_agent
    
    if wake_word_detector:
        wake_word_detector.stop()
    
    if voice_agent:
        voice_agent.cleanup()
