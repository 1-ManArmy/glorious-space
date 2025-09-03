/**
 * 2D Canvas Engine for Developer Crown Site
 * Provides interactive 2D drawing and visualization capabilities
 */

class Canvas2D {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.isDrawing = false;
        this.currentTool = 'pen';
        this.currentColor = '#000000';
        this.currentSize = 2;
        this.layers = [];
        this.currentLayer = 0;
        this.history = [];
        this.historyStep = -1;
        
        // WebSocket for real-time collaboration
        this.socket = null;
        this.sessionId = options.sessionId || null;
        this.isCollaborative = options.collaborative || false;
        
        this.init();
    }
    
    init() {
        this.setupCanvas();
        this.setupEventListeners();
        this.setupTools();
        this.createLayer();
        
        if (this.isCollaborative) {
            this.initWebSocket();
        }
    }
    
    setupCanvas() {
        // Set canvas size
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        
        // Set canvas styles
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        this.ctx.imageSmoothingEnabled = true;
        
        // Add canvas container styling
        this.canvas.style.cursor = 'crosshair';
        this.canvas.style.border = '2px solid #e1e5e9';
        this.canvas.style.borderRadius = '8px';
    }
    
    setupEventListeners() {
        // Mouse events
        this.canvas.addEventListener('mousedown', this.startDrawing.bind(this));
        this.canvas.addEventListener('mousemove', this.draw.bind(this));
        this.canvas.addEventListener('mouseup', this.stopDrawing.bind(this));
        this.canvas.addEventListener('mouseout', this.stopDrawing.bind(this));
        
        // Touch events for mobile
        this.canvas.addEventListener('touchstart', this.handleTouch.bind(this));
        this.canvas.addEventListener('touchmove', this.handleTouch.bind(this));
        this.canvas.addEventListener('touchend', this.stopDrawing.bind(this));
        
        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboard.bind(this));
        
        // Window resize
        window.addEventListener('resize', this.resizeCanvas.bind(this));
    }
    
    setupTools() {
        // Tool buttons
        const toolButtons = document.querySelectorAll('.tool-btn');
        toolButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setTool(e.target.dataset.tool);
                this.updateToolButtons(e.target);
            });
        });
        
        // Color picker
        const colorPicker = document.getElementById('colorPicker');
        if (colorPicker) {
            colorPicker.addEventListener('change', (e) => {
                this.currentColor = e.target.value;
            });
        }
        
        // Size slider
        const sizeSlider = document.getElementById('sizeSlider');
        if (sizeSlider) {
            sizeSlider.addEventListener('input', (e) => {
                this.currentSize = e.target.value;
                this.updateSizeDisplay();
            });
        }
        
        // Action buttons
        this.setupActionButtons();
    }
    
    setupActionButtons() {
        const clearBtn = document.getElementById('clearCanvas');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearCanvas());
        }
        
        const undoBtn = document.getElementById('undoBtn');
        if (undoBtn) {
            undoBtn.addEventListener('click', () => this.undo());
        }
        
        const redoBtn = document.getElementById('redoBtn');
        if (redoBtn) {
            redoBtn.addEventListener('click', () => this.redo());
        }
        
        const saveBtn = document.getElementById('saveCanvas');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveCanvas());
        }
        
        const loadBtn = document.getElementById('loadCanvas');
        if (loadBtn) {
            loadBtn.addEventListener('click', () => this.loadCanvas());
        }
    }
    
    setTool(tool) {
        this.currentTool = tool;
        
        switch(tool) {
            case 'pen':
                this.canvas.style.cursor = 'crosshair';
                break;
            case 'eraser':
                this.canvas.style.cursor = 'grab';
                break;
            case 'line':
                this.canvas.style.cursor = 'crosshair';
                break;
            case 'rectangle':
                this.canvas.style.cursor = 'crosshair';
                break;
            case 'circle':
                this.canvas.style.cursor = 'crosshair';
                break;
            default:
                this.canvas.style.cursor = 'default';
        }
    }
    
    updateToolButtons(activeBtn) {
        document.querySelectorAll('.tool-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        activeBtn.classList.add('active');
    }
    
    updateSizeDisplay() {
        const sizeDisplay = document.getElementById('sizeDisplay');
        if (sizeDisplay) {
            sizeDisplay.textContent = this.currentSize + 'px';
        }
    }
    
    getMousePos(e) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }
    
    startDrawing(e) {
        this.isDrawing = true;
        const pos = this.getMousePos(e);
        this.lastX = pos.x;
        this.lastY = pos.y;
        
        // Save state for undo functionality
        this.saveState();
        
        if (this.currentTool === 'pen' || this.currentTool === 'eraser') {
            this.ctx.beginPath();
            this.ctx.moveTo(pos.x, pos.y);
        }
    }
    
    draw(e) {
        if (!this.isDrawing) return;
        
        const pos = this.getMousePos(e);
        
        this.ctx.lineWidth = this.currentSize;
        this.ctx.strokeStyle = this.currentTool === 'eraser' ? '#FFFFFF' : this.currentColor;
        this.ctx.globalCompositeOperation = this.currentTool === 'eraser' ? 'destination-out' : 'source-over';
        
        switch(this.currentTool) {
            case 'pen':
            case 'eraser':
                this.ctx.lineTo(pos.x, pos.y);
                this.ctx.stroke();
                break;
                
            case 'line':
                this.redrawCanvas();
                this.ctx.beginPath();
                this.ctx.moveTo(this.lastX, this.lastY);
                this.ctx.lineTo(pos.x, pos.y);
                this.ctx.stroke();
                break;
                
            case 'rectangle':
                this.redrawCanvas();
                this.ctx.strokeRect(this.lastX, this.lastY, pos.x - this.lastX, pos.y - this.lastY);
                break;
                
            case 'circle':
                this.redrawCanvas();
                const radius = Math.sqrt(Math.pow(pos.x - this.lastX, 2) + Math.pow(pos.y - this.lastY, 2));
                this.ctx.beginPath();
                this.ctx.arc(this.lastX, this.lastY, radius, 0, 2 * Math.PI);
                this.ctx.stroke();
                break;
        }
        
        // Send updates for collaborative drawing
        if (this.isCollaborative && this.socket) {
            this.sendDrawingUpdate(pos);
        }
    }
    
    stopDrawing() {
        if (!this.isDrawing) return;
        this.isDrawing = false;
        this.ctx.globalCompositeOperation = 'source-over';
    }
    
    handleTouch(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 
                                        e.type === 'touchmove' ? 'mousemove' : 'mouseup', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        this.canvas.dispatchEvent(mouseEvent);
    }
    
    handleKeyboard(e) {
        if (e.ctrlKey) {
            switch(e.key) {
                case 'z':
                    e.preventDefault();
                    this.undo();
                    break;
                case 'y':
                    e.preventDefault();
                    this.redo();
                    break;
                case 's':
                    e.preventDefault();
                    this.saveCanvas();
                    break;
            }
        }
    }
    
    createLayer() {
        const layer = {
            id: Date.now(),
            name: `Layer ${this.layers.length + 1}`,
            visible: true,
            imageData: null
        };
        this.layers.push(layer);
    }
    
    saveState() {
        this.historyStep++;
        if (this.historyStep < this.history.length) {
            this.history.length = this.historyStep;
        }
        this.history.push(this.canvas.toDataURL());
    }
    
    undo() {
        if (this.historyStep > 0) {
            this.historyStep--;
            this.restoreCanvasFromHistory();
        }
    }
    
    redo() {
        if (this.historyStep < this.history.length - 1) {
            this.historyStep++;
            this.restoreCanvasFromHistory();
        }
    }
    
    restoreCanvasFromHistory() {
        const img = new Image();
        img.onload = () => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.drawImage(img, 0, 0);
        };
        img.src = this.history[this.historyStep];
    }
    
    clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.saveState();
    }
    
    redrawCanvas() {
        // This would redraw from layers in a more complex implementation
        // For now, we'll use the simple approach
    }
    
    resizeCanvas() {
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        this.ctx.putImageData(imageData, 0, 0);
    }
    
    // WebSocket for real-time collaboration
    initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/canvas/${this.sessionId}/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            console.log('Canvas WebSocket connected');
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleRemoteDrawing(data);
        };
        
        this.socket.onclose = () => {
            console.log('Canvas WebSocket disconnected');
        };
        
        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }
    
    sendDrawingUpdate(pos) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            const data = {
                type: 'drawing_update',
                tool: this.currentTool,
                color: this.currentColor,
                size: this.currentSize,
                position: pos,
                user: window.currentUser
            };
            this.socket.send(JSON.stringify(data));
        }
    }
    
    handleRemoteDrawing(data) {
        if (data.user === window.currentUser) return; // Don't apply own changes
        
        // Apply remote user's drawing
        const prevTool = this.currentTool;
        const prevColor = this.currentColor;
        const prevSize = this.currentSize;
        
        this.currentTool = data.tool;
        this.currentColor = data.color;
        this.currentSize = data.size;
        
        // Draw the remote user's stroke
        this.ctx.lineWidth = this.currentSize;
        this.ctx.strokeStyle = this.currentColor;
        this.ctx.lineTo(data.position.x, data.position.y);
        this.ctx.stroke();
        
        // Restore original settings
        this.currentTool = prevTool;
        this.currentColor = prevColor;
        this.currentSize = prevSize;
    }
    
    // Save and load functionality
    saveCanvas() {
        const canvasData = {
            imageData: this.canvas.toDataURL(),
            layers: this.layers,
            sessionId: this.sessionId,
            timestamp: new Date().toISOString()
        };
        
        // Send to backend
        fetch('/api/canvas/save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                session_id: this.sessionId,
                canvas_type: '2d',
                canvas_data: canvasData
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.showNotification('Canvas saved successfully!', 'success');
                if (data.session_id) {
                    this.sessionId = data.session_id;
                }
            } else {
                this.showNotification('Failed to save canvas', 'error');
            }
        })
        .catch(error => {
            console.error('Error saving canvas:', error);
            this.showNotification('Error saving canvas', 'error');
        });
    }
    
    loadCanvas() {
        // Implementation for loading saved canvas
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const img = new Image();
                    img.onload = () => {
                        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                        this.ctx.drawImage(img, 0, 0);
                        this.saveState();
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        };
        input.click();
    }
    
    exportCanvas(format = 'png') {
        const link = document.createElement('a');
        link.download = `canvas-${Date.now()}.${format}`;
        link.href = this.canvas.toDataURL(`image/${format}`);
        link.click();
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
    
    showNotification(message, type = 'info') {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 24px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            border-radius: 4px;
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize Canvas when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas2d');
    if (canvas) {
        const sessionId = canvas.dataset.sessionId;
        const collaborative = canvas.dataset.collaborative === 'true';
        
        window.canvas2d = new Canvas2D('canvas2d', {
            sessionId: sessionId,
            collaborative: collaborative
        });
    }
});
