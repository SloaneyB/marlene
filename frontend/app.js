// Marlene Smart Home Assistant - Frontend JavaScript

const API_URL = 'http://localhost:8000';

// UI Elements
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const manualBtn = document.getElementById('manual-btn');
const listeningStatus = document.getElementById('listening-status');
const processingStatus = document.getElementById('processing-status');
const activityLog = document.getElementById('activity-log');
const durationInput = document.getElementById('duration-input');
const apiStatus = document.getElementById('api-status');

// State
let isListening = false;
let isProcessing = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAPIConnection();
    setupEventListeners();
    startStatusUpdates();
});

// Check API Connection
async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_URL}/`);
        const data = await response.json();
        apiStatus.textContent = '✓ Connected';
        apiStatus.classList.add('connected');
        apiStatus.classList.remove('disconnected');
        addLogEntry('System connected to API', 'system');
    } catch (error) {
        apiStatus.textContent = '✗ Disconnected';
        apiStatus.classList.add('disconnected');
        apiStatus.classList.remove('connected');
        addLogEntry('Failed to connect to API. Make sure server.py is running.', 'error');
    }
}

// Setup Event Listeners
function setupEventListeners() {
    startBtn.addEventListener('click', startListening);
    stopBtn.addEventListener('click', stopListening);
    manualBtn.addEventListener('click', triggerManualCommand);
}

// Start Wake Word Listening
async function startListening() {
    try {
        startBtn.disabled = true;
        const response = await fetch(`${API_URL}/start-listening`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const data = await response.json();
            isListening = true;
            updateUI();
            addLogEntry('Wake word detection started', 'wake-word');
        } else {
            const error = await response.json();
            addLogEntry(`Error: ${error.message || 'Failed to start listening'}`, 'error');
            startBtn.disabled = false;
        }
    } catch (error) {
        addLogEntry(`Error: ${error.message}`, 'error');
        startBtn.disabled = false;
    }
}

// Stop Wake Word Listening
async function stopListening() {
    try {
        stopBtn.disabled = true;
        const response = await fetch(`${API_URL}/stop-listening`, {
            method: 'POST'
        });
        
        if (response.ok) {
            isListening = false;
            updateUI();
            addLogEntry('Wake word detection stopped', 'wake-word');
        } else {
            const error = await response.json();
            addLogEntry(`Error: ${error.message || 'Failed to stop listening'}`, 'error');
            stopBtn.disabled = false;
        }
    } catch (error) {
        addLogEntry(`Error: ${error.message}`, 'error');
        stopBtn.disabled = false;
    }
}

// Trigger Manual Command
async function triggerManualCommand() {
    try {
        manualBtn.disabled = true;
        const duration = parseInt(durationInput.value) || 5;
        
        addLogEntry(`Listening for ${duration} seconds...`, 'command');
        
        const response = await fetch(`${API_URL}/process-command`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ duration })
        });
        
        if (response.ok) {
            addLogEntry('Command processing complete', 'command');
        } else {
            const error = await response.json();
            addLogEntry(`Error: ${error.message || 'Failed to process command'}`, 'error');
        }
        
        manualBtn.disabled = false;
    } catch (error) {
        addLogEntry(`Error: ${error.message}`, 'error');
        manualBtn.disabled = false;
    }
}

// Update Status from API
async function updateStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        if (response.ok) {
            const status = await response.json();
            isListening = status.listening;
            isProcessing = status.processing;
            updateUI();
            
            // Log transcript if available
            if (status.last_transcript) {
                addLogEntry(`Transcript: ${status.last_transcript}`, 'command');
            }
        }
    } catch (error) {
        console.error('Failed to fetch status:', error);
    }
}

// Start periodic status updates
function startStatusUpdates() {
    setInterval(updateStatus, 1000);
}

// Update UI based on state
function updateUI() {
    // Update status indicators
    if (isListening) {
        listeningStatus.classList.add('active');
        listeningStatus.classList.remove('inactive');
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } else {
        listeningStatus.classList.add('inactive');
        listeningStatus.classList.remove('active');
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
    
    if (isProcessing) {
        processingStatus.classList.add('active');
        processingStatus.classList.remove('inactive');
        manualBtn.disabled = true;
    } else {
        processingStatus.classList.add('inactive');
        processingStatus.classList.remove('active');
        if (!isListening) {
            manualBtn.disabled = false;
        }
    }
}

// Add entry to activity log
function addLogEntry(message, type = 'info') {
    // Remove placeholder if it exists
    const placeholder = activityLog.querySelector('.placeholder');
    if (placeholder) {
        placeholder.remove();
    }
    
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    
    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.textContent = message;
    
    entry.appendChild(timestamp);
    entry.appendChild(messageDiv);
    
    activityLog.insertBefore(entry, activityLog.firstChild);
    
    // Keep only last 20 entries
    while (activityLog.children.length > 20) {
        activityLog.removeChild(activityLog.lastChild);
    }
}

// Initialize UI
updateUI();
