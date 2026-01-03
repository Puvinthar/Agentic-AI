/* Agentic AI Frontend - Main Application Script */

// Detect backend URL - works for both local and production
const getBackendURL = () => {
    // If we're on a deployed server, use the same host
    const protocol = window.location.protocol;
    const host = window.location.host;
    
    // For development (localhost:5000), backend is on localhost:8000
    if (host.includes('localhost') || host.includes('127.0.0.1')) {
        return 'http://localhost:8000';
    }
    
    // For production, assume backend is on same host with /api prefix
    // Or use environment variable if available
    return window.API_BACKEND_URL || `${protocol}//${host}`;
};

const API_BASE = '/api';
const BACKEND_URL = getBackendURL();
let conversationHistory = [];
let uploadedFile = null;

// Axios client configuration
const api = axios.create({
    baseURL: API_BASE,
    timeout: 30000, // default timeout; overrides per request when needed
});

const mapAxiosError = (error, fallbackMessage) => {
    if (error.response) {
        return `${fallbackMessage}: HTTP ${error.response.status}`;
    }
    if (error.code === 'ECONNABORTED') {
        return `${fallbackMessage}: Request timeout`;
    }
    return `${fallbackMessage}: ${error.message || 'Network error'}`;
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    checkBackendStatus();
    setupEventListeners();
    loadThemePreference();
    setInterval(checkBackendStatus, 30000); // Check every 30 seconds
});

function setupEventListeners() {
    const messageInput = document.getElementById('messageInput');
    messageInput.addEventListener('keypress', handleKeyPress);
    
    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });
}

// ============================================================================
// BACKEND STATUS
// ============================================================================

async function checkBackendStatus() {
    const statusElement = document.getElementById('backendStatus');
    const statusDot = statusElement.querySelector('.status-indicator');
    const statusText = statusElement.querySelector('.status-text');
    
    try {
        const response = await api.get('/health', { timeout: 10000 });
        
        if (response.status === 200) {
            statusElement.classList.add('online');
            statusElement.classList.remove('offline');
            statusText.textContent = 'Backend online';
        } else {
            statusElement.classList.remove('online');
            statusElement.classList.add('offline');
            statusText.textContent = 'Backend error';
        }
    } catch (error) {
        statusElement.classList.remove('online');
        statusElement.classList.add('offline');
        
        // Better error messages
        if (error.code === 'ECONNABORTED') {
            statusText.textContent = 'Backend starting...';
        } else if (error.response?.status === 503) {
            statusText.textContent = 'Backend warming up...';
        } else {
            statusText.textContent = 'Backend offline';
        }
        
        // Retry faster during startup
        setTimeout(checkBackendStatus, 3000);
    }
}

// ============================================================================
// MESSAGE HANDLING
// ============================================================================

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Disable input during sending
    messageInput.disabled = true;
    const sendBtn = document.querySelector('.send-btn-enhanced');
    if (sendBtn) sendBtn.disabled = true;
    
    // Hide welcome section if visible
    const welcomeSection = document.querySelector('.welcome-screen');
    if (welcomeSection) welcomeSection.style.display = 'none';
    
    // Add user message to display
    addMessage(message, 'user');
    conversationHistory.push({ role: 'user', content: message });
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Show loading indicator
    addLoadingMessage();
    
    try {
        const { data } = await api.post('/chat', {
            message: message,
            file: uploadedFile ? uploadedFile.name : null
        }, { timeout: 30000 });

        removeLoadingMessage();

        if (data.success) {
            const responseText = data.response || 'No response received';
            addMessage(responseText, 'bot');
            conversationHistory.push({ role: 'bot', content: responseText });
            addToChatHistory(message);
        } else {
            const errorMsg = data.error || data.message || 'Unknown error occurred';
            addMessage(`Error: ${errorMsg}`, 'error');
        }
    } catch (error) {
        removeLoadingMessage();
        const msg = mapAxiosError(error, 'Connection error');
        addMessage(msg, 'error');
        console.error('Error sending message:', error);
    } finally {
        messageInput.disabled = false;
        if (sendBtn) sendBtn.disabled = false;
        messageInput.focus();
    }
}

function addMessage(text, role) {
    const messageContainer = document.getElementById('messageContainer');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    // Create avatar icon
    const avatarEl = document.createElement('div');
    avatarEl.className = 'message-avatar';
    avatarEl.innerHTML = role === 'user' ? '👤' : '🤖';
    
    // Create message bubble
    const bubbleEl = document.createElement('div');
    bubbleEl.className = 'message-bubble';
    
    // Preserve formatting: convert line breaks to <br> and handle special characters
    const formattedText = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\*(.+?)\*/g, '<em>$1</em>'); // Italic
    
    bubbleEl.innerHTML = formattedText;
    
    // Assemble message (avatar position depends on role)
    if (role === 'user') {
        messageEl.appendChild(bubbleEl);
        messageEl.appendChild(avatarEl);
    } else {
        messageEl.appendChild(avatarEl);
        messageEl.appendChild(bubbleEl);
    }
    
    messageContainer.appendChild(messageEl);
    
    // Scroll to bottom
    messageContainer.parentElement.scrollTop = messageContainer.parentElement.scrollHeight;
}

function addLoadingMessage() {
    const messageContainer = document.getElementById('messageContainer');
    const messageEl = document.createElement('div');
    messageEl.className = 'message assistant loading';
    messageEl.id = 'loadingMessage';
    
    // Add avatar
    const avatarEl = document.createElement('div');
    avatarEl.className = 'message-avatar';
    avatarEl.innerHTML = '🤖';
    
    // Add loading bubble
    const bubbleEl = document.createElement('div');
    bubbleEl.className = 'message-bubble';
    bubbleEl.innerHTML = `
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    `;
    
    messageEl.appendChild(avatarEl);
    messageEl.appendChild(bubbleEl);
    
    messageContainer.appendChild(messageEl);
    messageContainer.parentElement.scrollTop = messageContainer.parentElement.scrollHeight;
}

function removeLoadingMessage() {
    const loadingEl = document.getElementById('loadingMessage');
    if (loadingEl) loadingEl.remove();
}

function addToChatHistory(message) {
    const chatHistory = document.getElementById('chatHistory');
    
    // Limit history items to 10
    const items = chatHistory.querySelectorAll('.chat-history-item');
    if (items.length >= 10) {
        items[items.length - 1].remove();
    }
    
    const historyItem = document.createElement('div');
    historyItem.className = 'chat-history-item';
    historyItem.textContent = message.substring(0, 30) + (message.length > 30 ? '...' : '');
    historyItem.onclick = () => loadChat(message);
    
    chatHistory.insertBefore(historyItem, chatHistory.firstChild);
}

// ============================================================================
// QUICK ACTIONS
// ============================================================================

function quickAction(message) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = message;
    messageInput.focus();
    sendMessage();
}

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const fileStatus = document.getElementById('fileStatus');
    
    // Validate file type
    const allowedExtensions = ['.pdf', '.txt', '.doc', '.docx'];
    const fileExt = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    const allowedMimes = ['application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (!allowedExtensions.includes(fileExt) && !allowedMimes.includes(file.type)) {
        fileStatus.textContent = '❌ Unsupported file type. Use PDF, TXT, or DOC';
        fileStatus.className = 'file-status error';
        event.target.value = ''; // Clear the input
        return;
    }
    
    // Validate file size (max 50MB)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        fileStatus.textContent = `❌ File too large. Max 50MB, your file is ${(file.size / 1024 / 1024).toFixed(1)}MB`;
        fileStatus.className = 'file-status error';
        event.target.value = ''; // Clear the input
        return;
    }
    
    fileStatus.textContent = '📤 Uploading...';
    fileStatus.className = 'file-status loading';
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const { data } = await api.post('/upload', formData, { timeout: 60000 });

        if (data.status === 'success' || data.success) {
            uploadedFile = file;
            fileStatus.textContent = `✅ File uploaded: ${file.name}`;
            fileStatus.className = 'file-status success';
            addMessage(`📄 Document "${file.name}" uploaded successfully! You can now ask questions about it.`, 'bot');
        } else {
            const errorMsg = data.message || data.error || 'Unknown error';
            fileStatus.textContent = `❌ Upload failed: ${errorMsg}`;
            fileStatus.className = 'file-status error';
        }
    } catch (error) {
        const msg = mapAxiosError(error, 'Upload error');
        fileStatus.textContent = `❌ ${msg}`;
        fileStatus.className = 'file-status error';
        console.error('File upload error:', error);
    } finally {
        event.target.value = ''; // Clear the input for next upload
    }
}

// ============================================================================
// MEETING MANAGEMENT
// ============================================================================

function toggleMeetingForm() {
    const modal = document.getElementById('meetingModal');
    modal.classList.toggle('active');
}

async function createMeeting() {
    const title = document.getElementById('meetingTitle').value.trim();
    const date = document.getElementById('meetingDate').value;
    const time = document.getElementById('meetingTime').value;
    const location = document.getElementById('meetingLocation').value.trim();
    const notes = document.getElementById('meetingNotes').value.trim();
    
    // Validation
    if (!title) {
        addMessage('❌ Meeting title is required', 'error');
        return;
    }
    
    if (!date) {
        addMessage('❌ Meeting date is required', 'error');
        return;
    }
    
    if (!time) {
        addMessage('❌ Meeting time is required', 'error');
        return;
    }
    
    if (!location) {
        addMessage('❌ Meeting location is required', 'error');
        return;
    }
    
    // Validate date is not in the past
    const selectedDateTime = new Date(`${date}T${time}`);
    if (selectedDateTime < new Date()) {
        addMessage('❌ Cannot schedule meeting in the past', 'error');
        return;
    }
    
    try {
        const { data } = await api.post('/meetings', {
            title,
            scheduled_date: `${date}T${time}:00`,
            location,
            description: notes || null
        }, { timeout: 15000 });

        if (data.status === 'success' || data.success) {
            const dateObj = new Date(`${date}T${time}`);
            const formattedDate = dateObj.toLocaleDateString('en-US', { 
                weekday: 'short', 
                month: 'short', 
                day: 'numeric' 
            });
            const formattedTime = dateObj.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit'
            });
            
            addMessage(`✅ Meeting created: "${title}" on ${formattedDate} at ${formattedTime} at ${location}`, 'bot');
            toggleMeetingForm();
            
            // Clear form
            document.getElementById('meetingTitle').value = '';
            document.getElementById('meetingDate').value = '';
            document.getElementById('meetingTime').value = '';
            document.getElementById('meetingLocation').value = '';
            document.getElementById('meetingNotes').value = '';
        } else {
            const errorMsg = data.message || data.error || 'Unknown error occurred';
            addMessage(`❌ Failed to create meeting: ${errorMsg}`, 'error');
        }
    } catch (error) {
        const msg = mapAxiosError(error, 'Error creating meeting');
        addMessage(`❌ ${msg}`, 'error');
        console.error('Meeting creation error:', error);
    }
}

// ============================================================================
// CHAT MANAGEMENT
// ============================================================================

function newChat() {
    // Clear conversation
    conversationHistory = [];
    document.getElementById('messageContainer').innerHTML = '';
    
    // Show welcome section
    const welcomeSection = document.querySelector('.welcome-section');
    if (welcomeSection) welcomeSection.style.display = 'flex';
    
    // Clear file
    uploadedFile = null;
    document.getElementById('fileStatus').textContent = '';
    
    // Focus input
    document.getElementById('messageInput').focus();
}

function loadChat(message) {
    document.getElementById('messageInput').value = message;
    document.getElementById('messageInput').focus();
}

// ============================================================================
// THEME TOGGLE
// ============================================================================

function loadThemePreference() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleSettings() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Optional: Show a brief notification
    const notification = document.createElement('div');
    notification.className = 'theme-notification';
    notification.textContent = `${newTheme === 'dark' ? '🌙' : '☀️'} ${newTheme.charAt(0).toUpperCase() + newTheme.slice(1)} theme`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 2000);
}
