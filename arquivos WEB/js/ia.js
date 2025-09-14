// Sistema de IA para QAT LAB
class QATLabIA {
    constructor() {
        this.webcamStream = null;
        this.isWebcamActive = false;
        this.chatHistory = [];
        this.uploadedFiles = new Map();
        this.initializeIA();
    }

    initializeIA() {
        this.setupFileUpload();
        this.setupChatbot();
        this.loadKnowledgeBase();
    }

    // Sistema de Upload de Arquivos
    setupFileUpload() {
        const fileInput = document.getElementById('fileInput');
        const iaFileInput = document.getElementById('iaFileInput');
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileUpload(e, 'general'));
        }
        
        if (iaFileInput) {
            iaFileInput.addEventListener('change', (e) => this.handleFileUpload(e, 'ia'));
        }
        
        // Drag and drop
        document.addEventListener('dragover', (e) => {
            e.preventDefault();
        });
        
        document.addEventListener('drop', (e) => {
            e.preventDefault();
            this.handleFileDrop(e);
        });
    }

    handleFileUpload(event, type) {
        const files = Array.from(event.target.files);
        const containerId = type === 'ia' ? 'iaUploadedFiles' : 'uploadedFiles';
        
        files.forEach(file => {
            this.processFile(file, containerId);
        });
    }

    handleFileDrop(event) {
        const files = Array.from(event.dataTransfer.files);
        files.forEach(file => {
            this.processFile(file, 'uploadedFiles');
        });
    }

    processFile(file, containerId) {
        const fileId = Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        const fileData = {
            id: fileId,
            name: file.name,
            size: file.size,
            type: file.type,
            uploadDate: new Date(),
            content: null
        };

        // Salvar no localStorage
        this.uploadedFiles.set(fileId, fileData);
        this.saveFilesToStorage();
        
        // Ler conteúdo do arquivo se for texto
        if (file.type.includes('text') || file.name.endsWith('.csv')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                fileData.content = e.target.result;
                this.uploadedFiles.set(fileId, fileData);
                this.saveFilesToStorage();
            };
            reader.readAsText(file);
        }
        
        this.displayUploadedFile(fileData, containerId);
        this.showNotification('Arquivo enviado com sucesso!', 'success');
    }

    displayUploadedFile(fileData, containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.style.display = 'block';
        
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-info">
                <i class="fas fa-file"></i>
                <span>${fileData.name}</span>
                <small>(${this.formatFileSize(fileData.size)})</small>
            </div>
            <button class="remove-file" onclick="qatIA.removeFile('${fileData.id}', '${containerId}')">
                <i class="fas fa-trash"></i>
            </button>
        `;
        
        container.appendChild(fileItem);
    }

    removeFile(fileId, containerId) {
        this.uploadedFiles.delete(fileId);
        this.saveFilesToStorage();
        
        const container = document.getElementById(containerId);
        const fileItems = container.querySelectorAll('.file-item');
        fileItems.forEach(item => {
            if (item.querySelector('button').onclick.toString().includes(fileId)) {
                item.remove();
            }
        });
        
        if (container.children.length === 0) {
            container.style.display = 'none';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    saveFilesToStorage() {
        const filesArray = Array.from(this.uploadedFiles.entries());
        localStorage.setItem('qatlab_uploaded_files', JSON.stringify(filesArray));
    }

    loadFilesFromStorage() {
        const stored = localStorage.getItem('qatlab_uploaded_files');
        if (stored) {
            const filesArray = JSON.parse(stored);
            this.uploadedFiles = new Map(filesArray);
        }
    }

    // Sistema de Chatbot IA
    setupChatbot() {
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });
        }
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Adicionar mensagem do usuário
        this.addMessageToChat(message, 'user');
        input.value = '';
        
        // Simular digitação
        this.showTypingIndicator();
        
        // Processar resposta da IA
        setTimeout(() => {
            const response = this.processAIResponse(message);
            this.hideTypingIndicator();
            this.addMessageToChat(response, 'bot');
        }, 1000 + Math.random() * 2000);
    }

    addMessageToChat(message, sender) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `
            <div class="message-content">${message}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Salvar no histórico
        this.chatHistory.push({ message, sender, timestamp: new Date() });
        this.saveChatHistory();
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-circle"></i>
                <i class="fas fa-circle"></i>
                <i class="fas fa-circle"></i>
                Digitando...
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    processAIResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // Base de conhecimento química
        const responses = {
            'olá': 'Olá! Sou o assistente virtual do QAT LAB. Como posso ajudá-lo com questões químicas hoje?',
            'oi': 'Oi! Estou aqui para ajudar com análises químicas e gerenciamento do laboratório.',
            'substância': 'Posso ajudar com informações sobre substâncias químicas. Que substância específica você gostaria de conhecer?',
            'equipamento': 'Sobre equipamentos de laboratório, posso fornecer informações sobre manutenção, calibração e uso adequado.',
            'segurança': 'A segurança no laboratório é fundamental. Sempre use EPIs adequados e siga os protocolos de segurança.',
            'ph': 'O pH é uma medida da acidez ou basicidade de uma solução, variando de 0 a 14.',
            'titulação': 'A titulação é uma técnica analítica para determinar a concentração de uma solução.',
            'espectroscopia': 'A espectroscopia é uma técnica que analisa a interação da radiação eletromagnética com a matéria.',
            'cromatografia': 'A cromatografia é uma técnica de separação baseada na distribuição diferencial dos componentes.',
            'massa molar': 'A massa molar é a massa de um mol de uma substância, expressa em g/mol.',
            'estequiometria': 'A estequiometria estuda as relações quantitativas entre reagentes e produtos em reações químicas.',
            'default': 'Interessante pergunta! Baseado no meu conhecimento químico, recomendo consultar literatura especializada ou realizar testes experimentais para uma resposta mais precisa.'
        };
        
        // Buscar resposta mais adequada
        for (const [key, response] of Object.entries(responses)) {
            if (lowerMessage.includes(key) && key !== 'default') {
                return response;
            }
        }
        
        // Análise de arquivos enviados
        if (lowerMessage.includes('arquivo') || lowerMessage.includes('documento')) {
            const fileCount = this.uploadedFiles.size;
            if (fileCount > 0) {
                return `Vejo que você tem ${fileCount} arquivo(s) enviado(s). Posso analisar documentos em PDF, texto e planilhas para extrair informações químicas relevantes.`;
            } else {
                return 'Você pode enviar arquivos para análise usando a área de upload. Aceito PDFs, documentos de texto e planilhas.';
            }
        }
        
        return responses.default;
    }

    saveChatHistory() {
        localStorage.setItem('qatlab_chat_history', JSON.stringify(this.chatHistory));
    }

    loadChatHistory() {
        const stored = localStorage.getItem('qatlab_chat_history');
        if (stored) {
            this.chatHistory = JSON.parse(stored);
        }
    }

    // Sistema de Webcam
    async startWebcam() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 } 
            });
            
            this.webcamStream = stream;
            this.isWebcamActive = true;
            
            const preview = document.getElementById('webcamPreview');
            const video = document.createElement('video');
            video.srcObject = stream;
            video.autoplay = true;
            video.style.width = '100%';
            video.style.height = '100%';
            video.style.objectFit = 'cover';
            
            preview.innerHTML = '';
            preview.appendChild(video);
            
            // Atualizar botões
            const startBtn = document.querySelector('.btn-webcam:not(.stop)');
            const stopBtn = document.querySelector('.btn-webcam.stop');
            if (startBtn) startBtn.style.display = 'none';
            if (stopBtn) stopBtn.style.display = 'inline-block';
            
            this.showNotification('Câmera iniciada com sucesso!', 'success');
            
            // Iniciar detecção de objetos (simulada)
            this.startObjectDetection(video);
            
        } catch (error) {
            console.error('Erro ao acessar webcam:', error);
            this.showNotification('Erro ao acessar a câmera. Verifique as permissões.', 'error');
        }
    }

    stopWebcam() {
        if (this.webcamStream) {
            this.webcamStream.getTracks().forEach(track => track.stop());
            this.webcamStream = null;
            this.isWebcamActive = false;
            
            const preview = document.getElementById('webcamPreview');
            preview.innerHTML = `
                <div>
                    <i class="fas fa-camera" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <p>Clique em "Iniciar Câmera" para começar</p>
                </div>
            `;
            
            // Atualizar botões
            const startBtn = document.querySelector('.btn-webcam:not(.stop)');
            const stopBtn = document.querySelector('.btn-webcam.stop');
            if (startBtn) startBtn.style.display = 'inline-block';
            if (stopBtn) stopBtn.style.display = 'none';
            
            this.showNotification('Câmera desligada.', 'info');
        }
    }

    captureImage() {
        if (!this.isWebcamActive) {
            this.showNotification('Inicie a câmera primeiro.', 'warning');
            return;
        }
        
        const video = document.querySelector('#webcamPreview video');
        if (!video) return;
        
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        // Converter para blob e salvar
        canvas.toBlob((blob) => {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const filename = `capture_${timestamp}.png`;
            
            // Simular salvamento
            this.saveCapture(blob, filename);
            this.showNotification('Imagem capturada com sucesso!', 'success');
        }, 'image/png');
    }

    saveCapture(blob, filename) {
        // Criar URL para download
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    startObjectDetection(video) {
        // Simulação de detecção de objetos
        const detectObjects = () => {
            if (!this.isWebcamActive) return;
            
            // Simular detecção aleatória
            if (Math.random() > 0.7) {
                const objects = ['Béquer', 'Pipeta', 'Erlenmeyer', 'Proveta', 'Balança'];
                const detected = objects[Math.floor(Math.random() * objects.length)];
                
                // Mostrar detecção na interface
                this.showObjectDetection(detected);
            }
            
            setTimeout(detectObjects, 2000);
        };
        
        setTimeout(detectObjects, 1000);
    }

    showObjectDetection(objectName) {
        const preview = document.getElementById('webcamPreview');
        const existing = preview.querySelector('.detection-overlay');
        if (existing) existing.remove();
        
        const overlay = document.createElement('div');
        overlay.className = 'detection-overlay';
        overlay.style.cssText = `
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(102, 126, 234, 0.9);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8rem;
            z-index: 10;
        `;
        overlay.textContent = `🔍 Detectado: ${objectName}`;
        
        preview.style.position = 'relative';
        preview.appendChild(overlay);
        
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
            }
        }, 3000);
    }

    loadKnowledgeBase() {
        // Carregar base de conhecimento química
        this.knowledgeBase = {
            substances: {
                'h2o': { name: 'Água', formula: 'H₂O', molarMass: 18.015 },
                'nacl': { name: 'Cloreto de Sódio', formula: 'NaCl', molarMass: 58.44 },
                'h2so4': { name: 'Ácido Sulfúrico', formula: 'H₂SO₄', molarMass: 98.079 }
            },
            equipment: {
                'beaker': { name: 'Béquer', category: 'Vidraria', use: 'Medição e mistura' },
                'pipette': { name: 'Pipeta', category: 'Vidraria', use: 'Transferência precisa' }
            }
        };
    }

    showNotification(message, type = 'info') {
        // Usar sistema de notificação existente
        if (typeof showNotification === 'function') {
            showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }
}

// Inicializar sistema de IA
let qatIA;
document.addEventListener('DOMContentLoaded', () => {
    qatIA = new QATLabIA();
});

// Funções globais para compatibilidade
function sendMessage() {
    if (qatIA) qatIA.sendMessage();
}

function startWebcam() {
    if (qatIA) qatIA.startWebcam();
}

function stopWebcam() {
    if (qatIA) qatIA.stopWebcam();
}

function captureImage() {
    if (qatIA) qatIA.captureImage();
}