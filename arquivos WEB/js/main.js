// Sistema QAT LAB - JavaScript Principal

// Variáveis globais
let currentPage = 'welcome';
let database = {
    substancias: [],
    equipamentos: [],
    projetos: [],
    estoque: [],
    atividades: []
};

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    loadDatabase();
    updateStats();
    setupForms();
    updateAllTables();
});

// Navegação entre páginas
function showPage(pageName) {
    // Esconder todas as páginas
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Remover classe active dos botões de navegação
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Mostrar página selecionada
    const targetPage = document.getElementById(pageName + '-page');
    if (targetPage) {
        targetPage.classList.add('active');
        currentPage = pageName;
        updateStats();
        
        // Atualizar tabelas específicas quando necessário
        if (pageName === 'substancias') {
            updateSubstanciasTable();
            setupSubstanciasForm();
        } else if (pageName === 'equipamentos') {
            updateEquipamentosTable();
            setupEquipamentosForm();
            updateEquipamentosSelect();
        } else if (pageName === 'projetos') {
            updateProjetosTable();
            setupProjetosForm();
        } else if (pageName === 'estoque') {
            updateEstoqueTable();
            setupEstoqueForm();
        } else if (pageName === 'dashboard') {
            setTimeout(() => {
                createDashboardCharts();
            }, 100);
        } else if (pageName === 'ia') {
            setupIAPage();
        }
    }
}

// Configurar formulários
function setupForms() {
    setupSubstanciasForm();
    setupEquipamentosForm();
    setupProjetosForm();
    setupEstoqueForm();
}

// === SUBSTÂNCIAS ===

// Adicionar substância
function adicionarSubstancia() {
    const nome = document.getElementById('nome').value;
    const formula = document.getElementById('formula').value;
    
    if (nome && formula) {
        const substancia = {
            id: Date.now(),
            nome: nome,
            formula: formula,
            data: new Date().toLocaleDateString('pt-BR')
        };
        
        database.substancias.push(substancia);
        saveDatabase();
        updateSubstanciasTable();
        updateStats();
        document.getElementById('substancia-form').reset();
        showNotification('Substância adicionada com sucesso!', 'success');
    }
}

// Atualizar tabela de substâncias
function updateSubstanciasTable() {
    const tbody = document.querySelector('#substancias-table tbody');
    if (!tbody) return;
    
    tbody.innerHTML = database.substancias.map(substancia => `
        <tr>
            <td>${substancia.nome}</td>
            <td>${substancia.formula}</td>
            <td>
                <button onclick="editarSubstancia(${substancia.id})" class="btn btn-warning btn-sm">Editar</button>
                <button onclick="removerSubstancia(${substancia.id})" class="btn btn-danger btn-sm">Remover</button>
            </td>
        </tr>
    `).join('');
}

// Editar substância
function editarSubstancia(id) {
    const substancia = database.substancias.find(s => s.id === id);
    if (substancia) {
        document.getElementById('nome').value = substancia.nome;
        document.getElementById('formula').value = substancia.formula;
        removerSubstancia(id);
    }
}

// Remover substância
function removerSubstancia(id) {
    if (confirm('Tem certeza que deseja remover esta substância?')) {
        database.substancias = database.substancias.filter(s => s.id !== id);
        saveDatabase();
        updateSubstanciasTable();
        updateStats();
        showNotification('Substância removida!', 'info');
    }
}

// === EQUIPAMENTOS ===

// Adicionar equipamento
function adicionarEquipamento() {
    const nome = prompt('Nome do equipamento:');
    const tipo = prompt('Tipo do equipamento:');
    const status = prompt('Status (Operacional/Manutenção/Inoperante):') || 'Operacional';
    
    if (nome && tipo) {
        const equipamento = {
            id: Date.now(),
            nome: nome,
            tipo: tipo,
            status: status,
            data: new Date().toLocaleDateString('pt-BR')
        };
        
        database.equipamentos.push(equipamento);
        saveDatabase();
        updateEquipamentosTable();
        updateStats();
        showNotification('Equipamento adicionado com sucesso!', 'success');
    }
}

// Atualizar tabela de equipamentos
function updateEquipamentosTable() {
    const container = document.getElementById('equipamentos-page');
    if (!container) return;
    
    container.innerHTML = `
        <div class="equipamentos-container">
            <h2>Controle de Equipamentos</h2>
            <div class="form-actions">
                <button onclick="adicionarEquipamento()" class="btn btn-primary">Adicionar Equipamento</button>
            </div>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Tipo</th>
                            <th>Status</th>
                            <th>Data</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${database.equipamentos.map(eq => `
                            <tr>
                                <td>${eq.nome}</td>
                                <td>${eq.tipo}</td>
                                <td><span class="status-badge status-${eq.status.toLowerCase()}">${eq.status}</span></td>
                                <td>${eq.data}</td>
                                <td>
                                    <button onclick="editarEquipamento(${eq.id})" class="btn btn-warning btn-sm">Editar</button>
                                    <button onclick="removerEquipamento(${eq.id})" class="btn btn-danger btn-sm">Remover</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

// Editar equipamento
function editarEquipamento(id) {
    const equipamento = database.equipamentos.find(eq => eq.id === id);
    if (equipamento) {
        const nome = prompt('Nome do equipamento:', equipamento.nome);
        const tipo = prompt('Tipo do equipamento:', equipamento.tipo);
        const status = prompt('Status:', equipamento.status);
        
        if (nome && tipo) {
            equipamento.nome = nome;
            equipamento.tipo = tipo;
            equipamento.status = status;
            saveDatabase();
            updateEquipamentosTable();
            updateStats();
            showNotification('Equipamento atualizado!', 'success');
        }
    }
}

// Remover equipamento
function removerEquipamento(id) {
    if (confirm('Tem certeza que deseja remover este equipamento?')) {
        database.equipamentos = database.equipamentos.filter(eq => eq.id !== id);
        saveDatabase();
        updateEquipamentosTable();
        updateStats();
        showNotification('Equipamento removido!', 'info');
    }
}

// === PROJETOS ===

// Adicionar projeto
function adicionarProjeto() {
    const titulo = prompt('Título do projeto:');
    const coordenador = prompt('Coordenador:');
    const area = prompt('Área de pesquisa:');
    const status = prompt('Status (Planejamento/Andamento/Concluído):') || 'Planejamento';
    
    if (titulo && coordenador) {
        const projeto = {
            id: Date.now(),
            titulo: titulo,
            coordenador: coordenador,
            area: area,
            status: status,
            data: new Date().toLocaleDateString('pt-BR')
        };
        
        database.projetos.push(projeto);
        saveDatabase();
        updateProjetosTable();
        updateStats();
        showNotification('Projeto adicionado com sucesso!', 'success');
    }
}

// Atualizar tabela de projetos
function updateProjetosTable() {
    const container = document.getElementById('projetos-page');
    if (!container) return;
    
    container.innerHTML = `
        <div class="projetos-container">
            <h2>Gerenciamento de Projetos</h2>
            <div class="form-actions">
                <button onclick="adicionarProjeto()" class="btn btn-primary">Adicionar Projeto</button>
            </div>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Título</th>
                            <th>Coordenador</th>
                            <th>Área</th>
                            <th>Status</th>
                            <th>Data</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${database.projetos.map(proj => `
                            <tr>
                                <td>${proj.titulo}</td>
                                <td>${proj.coordenador}</td>
                                <td>${proj.area}</td>
                                <td><span class="status-badge status-${proj.status.toLowerCase()}">${proj.status}</span></td>
                                <td>${proj.data}</td>
                                <td>
                                    <button onclick="editarProjeto(${proj.id})" class="btn btn-warning btn-sm">Editar</button>
                                    <button onclick="removerProjeto(${proj.id})" class="btn btn-danger btn-sm">Remover</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

// Editar projeto
function editarProjeto(id) {
    const projeto = database.projetos.find(p => p.id === id);
    if (projeto) {
        const titulo = prompt('Título do projeto:', projeto.titulo);
        const coordenador = prompt('Coordenador:', projeto.coordenador);
        const area = prompt('Área de pesquisa:', projeto.area);
        const status = prompt('Status:', projeto.status);
        
        if (titulo && coordenador) {
            projeto.titulo = titulo;
            projeto.coordenador = coordenador;
            projeto.area = area;
            projeto.status = status;
            saveDatabase();
            updateProjetosTable();
            updateStats();
            showNotification('Projeto atualizado!', 'success');
        }
    }
}

// Remover projeto
function removerProjeto(id) {
    if (confirm('Tem certeza que deseja remover este projeto?')) {
        database.projetos = database.projetos.filter(p => p.id !== id);
        saveDatabase();
        updateProjetosTable();
        updateStats();
        showNotification('Projeto removido!', 'info');
    }
}

// === ESTOQUE ===

// Adicionar item ao estoque
function adicionarEstoque() {
    const nome = prompt('Nome do item:');
    const quantidade = prompt('Quantidade:');
    const unidade = prompt('Unidade (g, ml, unidades):') || 'unidades';
    
    if (nome && quantidade) {
        const item = {
            id: Date.now(),
            nome: nome,
            quantidade: parseFloat(quantidade),
            unidade: unidade,
            data: new Date().toLocaleDateString('pt-BR')
        };
        
        database.estoque.push(item);
        saveDatabase();
        updateEstoqueTable();
        updateStats();
        showNotification('Item adicionado ao estoque!', 'success');
    }
}

// Atualizar tabela de estoque
function updateEstoqueTable() {
    const container = document.getElementById('estoque-page');
    if (!container) return;
    
    container.innerHTML = `
        <div class="estoque-container">
            <h2>Controle de Estoque</h2>
            <div class="form-actions">
                <button onclick="adicionarEstoque()" class="btn btn-primary">Adicionar Item</button>
            </div>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Quantidade</th>
                            <th>Unidade</th>
                            <th>Data</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${database.estoque.map(item => `
                            <tr>
                                <td>${item.nome}</td>
                                <td>${item.quantidade}</td>
                                <td>${item.unidade}</td>
                                <td>${item.data}</td>
                                <td>
                                    <button onclick="editarEstoque(${item.id})" class="btn btn-warning btn-sm">Editar</button>
                                    <button onclick="removerEstoque(${item.id})" class="btn btn-danger btn-sm">Remover</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
    `;
}

// Editar item do estoque
function editarEstoque(id) {
    const item = database.estoque.find(i => i.id === id);
    if (item) {
        const nome = prompt('Nome do item:', item.nome);
        const quantidade = prompt('Quantidade:', item.quantidade);
        const unidade = prompt('Unidade:', item.unidade);
        
        if (nome && quantidade) {
            item.nome = nome;
            item.quantidade = parseFloat(quantidade);
            item.unidade = unidade;
            saveDatabase();
            updateEstoqueTable();
            updateStats();
            showNotification('Item atualizado!', 'success');
        }
    }
}

// Remover item do estoque
function removerEstoque(id) {
    if (confirm('Tem certeza que deseja remover este item?')) {
        database.estoque = database.estoque.filter(i => i.id !== id);
        saveDatabase();
        updateEstoqueTable();
        updateStats();
        showNotification('Item removido!', 'info');
    }
}

// === IA ===

function showIATab(tabName) {
    // Remover classe active de todos os botões e painéis
    document.querySelectorAll('.ia-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.ia-panel').forEach(panel => panel.classList.remove('active'));
    
    // Ativar botão e painel selecionados
    event.target.classList.add('active');
    document.getElementById(tabName + '-tab').classList.add('active');
}

function setupIAPage() {
    // Configurar chatbot
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.focus();
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const messagesContainer = document.getElementById('chat-messages');
    
    if (!input.value.trim()) return;
    
    // Adicionar mensagem do usuário
    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.innerHTML = `<div class="message-content">${input.value}</div>`;
    messagesContainer.appendChild(userMessage);
    
    // Simular resposta do bot
    setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot-message';
        botMessage.innerHTML = `<div class="message-content">Obrigado pela sua pergunta! Esta é uma resposta simulada do chatbot.</div>`;
        messagesContainer.appendChild(botMessage);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 1000);
    
    input.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function startDetection() {
    showNotification('Detector de objetos iniciado (simulação)', 'info');
}

function stopDetection() {
    showNotification('Detector de objetos parado', 'info');
}

// === CALCULADORA ===

// Calculadora - Mostrar calculadora
function showCalculator(type) {
    document.querySelectorAll('.calculator-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(type + '-calc').classList.add('active');
    event.target.classList.add('active');
}

// Calcular massa molar
function calcularMassaMolar() {
    const formula = document.getElementById('formula-molar').value.trim();
    const resultado = document.getElementById('resultado-molar');
    
    if (!formula) {
        resultado.innerHTML = '<p class="error">Por favor, insira uma fórmula química.</p>';
        return;
    }
    
    try {
        // Tabela periódica simplificada
        const elementos = {
            'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
            'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
            'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
            'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
            'Fe': 55.845, 'Cu': 63.546, 'Zn': 65.38, 'Br': 79.904, 'I': 126.904
        };
        
        let massaMolar = 0;
        const regex = /([A-Z][a-z]?)(\d*)/g;
        let match;
        
        while ((match = regex.exec(formula)) !== null) {
            const elemento = match[1];
            const quantidade = parseInt(match[2]) || 1;
            
            if (elementos[elemento]) {
                massaMolar += elementos[elemento] * quantidade;
            } else {
                throw new Error(`Elemento ${elemento} não encontrado`);
            }
        }
        
        resultado.innerHTML = `
            <div class="resultado-success">
                <h4>Resultado:</h4>
                <p><strong>Fórmula:</strong> ${formula}</p>
                <p><strong>Massa Molar:</strong> ${massaMolar.toFixed(3)} g/mol</p>
            </div>
        `;
    } catch (error) {
        resultado.innerHTML = `<p class="error">Erro: ${error.message}</p>`;
    }
}

// Calcular concentração
function calcularConcentracao() {
    const massa = parseFloat(document.getElementById('massa-soluto').value);
    const volume = parseFloat(document.getElementById('volume-solucao').value);
    const resultado = document.getElementById('resultado-concentracao');
    
    if (isNaN(massa) || isNaN(volume) || volume <= 0) {
        resultado.innerHTML = '<p class="error">Por favor, insira valores válidos.</p>';
        return;
    }
    
    const concentracao = massa / volume;
    
    resultado.innerHTML = `
        <div class="resultado-success">
            <h4>Resultado:</h4>
            <p><strong>Massa do Soluto:</strong> ${massa} g</p>
            <p><strong>Volume da Solução:</strong> ${volume} L</p>
            <p><strong>Concentração:</strong> ${concentracao.toFixed(3)} g/L</p>
        </div>
    `;
}

// === DASHBOARD ===

function createDashboardCharts() {
    createSubstanciasChart();
    createEquipamentosChart();
}

function createSubstanciasChart() {
    const ctx = document.getElementById('substanciasChart');
    if (!ctx) return;
    
    // Agrupar substâncias por tipo (baseado na primeira letra da fórmula)
    const tipos = {};
    database.substancias.forEach(sub => {
        const tipo = sub.formula ? sub.formula.charAt(0) : 'Outros';
        tipos[tipo] = (tipos[tipo] || 0) + 1;
    });
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(tipos),
            datasets: [{
                data: Object.values(tipos),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                    '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createEquipamentosChart() {
    const ctx = document.getElementById('equipamentosChart');
    if (!ctx) return;
    
    // Agrupar equipamentos por status
    const status = {};
    database.equipamentos.forEach(eq => {
        const st = eq.status || 'Não definido';
        status[st] = (status[st] || 0) + 1;
    });
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(status),
            datasets: [{
                label: 'Quantidade',
                data: Object.values(status),
                backgroundColor: [
                    '#4CAF50', '#FF9800', '#F44336', '#9E9E9E'
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// === BANCO DE DADOS ===

// Carregar dados do localStorage
function loadDatabase() {
    const savedData = localStorage.getItem('qatlab_database');
    if (savedData) {
        database = JSON.parse(savedData);
    }
}

// Salvar dados no localStorage
function saveDatabase() {
    localStorage.setItem('qatlab_database', JSON.stringify(database));
}

// Atualizar estatísticas
function updateStats() {
    const totalSubstancias = document.getElementById('total-substancias');
    const totalEquipamentos = document.getElementById('total-equipamentos');
    const totalProjetos = document.getElementById('total-projetos');
    const totalEstoque = document.getElementById('total-estoque');
    
    if (totalSubstancias) totalSubstancias.textContent = database.substancias.length;
    if (totalEquipamentos) totalEquipamentos.textContent = database.equipamentos.length;
    if (totalProjetos) totalProjetos.textContent = database.projetos.length;
    if (totalEstoque) totalEstoque.textContent = database.estoque.length;
}

// Atualizar todas as tabelas
function updateAllTables() {
    updateSubstanciasTable();
    updateEquipamentosTable();
    updateProjetosTable();
    updateEstoqueTable();
}

// Carregar banco de dados
function loadDatabase() {
    const savedData = localStorage.getItem('qatlab_database');
    if (savedData) {
        database = JSON.parse(savedData);
    }
}

// Salvar banco de dados
function saveDatabase() {
    localStorage.setItem('qatlab_database', JSON.stringify(database));
}

// === NOTIFICAÇÕES ===

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (notification) {
        notification.textContent = message;
        notification.className = `notification ${type} show`;
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
}

// Exportar dados (função adicional)
function exportarDados() {
    const dados = JSON.stringify(database, null, 2);
    const blob = new Blob([dados], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'qatlab_backup.json';
    a.click();
    URL.revokeObjectURL(url);
    showNotification('Dados exportados com sucesso!', 'success');
}

// Importar dados (função adicional)
function importarDados() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const dados = JSON.parse(e.target.result);
                    database = dados;
                    saveDatabase();
                    updateStats();
                    updateSubstanciasTable();
                    showNotification('Dados importados com sucesso!', 'success');
                } catch (error) {
                    showNotification('Erro ao importar dados!', 'error');
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}

// Função para renderizar status com ícones
function renderStatusBadge(status, type = 'equipment') {
    const statusMap = {
        equipment: {
            'operacional': 'status-operacional',
            'manutenção': 'status-manutenção', 
            'inoperante': 'status-inoperante'
        },
        project: {
            'planejamento': 'status-planejamento',
            'andamento': 'status-andamento',
            'concluído': 'status-concluído'
        },
        substance: {
            'disponível': 'status-disponivel',
            'esgotado': 'status-esgotado',
            'baixo estoque': 'status-baixo-estoque'
        }
    };
    
    const statusClass = statusMap[type][status.toLowerCase()] || 'status-badge';
    return `<span class="status-badge ${statusClass}">${status}</span>`;
}

// Atualizar função de renderização de substâncias
function atualizarTabelaSubstancias() {
    const tbody = document.querySelector('#substancias-table tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    database.substancias.forEach((substancia, index) => {
        const row = document.createElement('tr');
        
        // Determinar status baseado na quantidade
        let status = 'disponível';
        if (substancia.quantidade <= 0) {
            status = 'esgotado';
        } else if (substancia.quantidade < 10) {
            status = 'baixo estoque';
        }
        
        row.innerHTML = `
            <td>${substancia.nome}</td>
            <td>${substancia.formula}</td>
            <td>${substancia.massaMolar} g/mol</td>
            <td>${substancia.densidade} g/cm³</td>
            <td>${substancia.pontoFusao}°C</td>
            <td>${substancia.pontoEbulicao}°C</td>
            <td>${substancia.quantidade || 0} ${substancia.unidade || 'g'}</td>
            <td>${renderStatusBadge(status, 'substance')}</td>
            <td>
                <button class="btn btn-secondary" onclick="editarSubstancia(${index})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-danger" onclick="removerSubstancia(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Atualizar função de renderização de equipamentos
function atualizarTabelaEquipamentos() {
    const tbody = document.querySelector('#equipamentos-table tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    database.equipamentos.forEach((equipamento, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${equipamento.nome}</td>
            <td>${equipamento.tipo}</td>
            <td>${equipamento.marca}</td>
            <td>${equipamento.modelo}</td>
            <td>${equipamento.localizacao}</td>
            <td>${renderStatusBadge(equipamento.status, 'equipment')}</td>
            <td>${equipamento.ultimaManutencao || 'N/A'}</td>
            <td>
                <button class="btn btn-secondary" onclick="editarEquipamento(${index})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-danger" onclick="removerEquipamento(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}