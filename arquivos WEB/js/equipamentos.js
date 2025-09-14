// Gerenciamento de Equipamentos - Versão Completa
class EquipamentosManager {
    constructor() {
        this.equipamentos = this.carregarEquipamentos();
        this.manutencoes = this.carregarManutencoes();
        this.initEventListeners();
        this.renderizarTabela();
        this.atualizarListaEquipamentos();
    }

    initEventListeners() {
        // Formulário de equipamentos
        const equipmentForm = document.getElementById('equipment-form');
        if (equipmentForm) {
            equipmentForm.addEventListener('submit', (e) => this.adicionarEquipamento(e));
        }

        // Formulário de manutenção
        const maintenanceForm = document.getElementById('maintenance-form');
        if (maintenanceForm) {
            maintenanceForm.addEventListener('submit', (e) => this.adicionarManutencao(e));
        }

        // Filtros
        const searchInput = document.getElementById('search-equipment');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.filtrarEquipamentos(e.target.value));
        }

        const filterStatus = document.getElementById('filter-status');
        if (filterStatus) {
            filterStatus.addEventListener('change', (e) => this.filtrarPorStatus(e.target.value));
        }
    }

    carregarEquipamentos() {
        const equipamentos = localStorage.getItem('qat_equipamentos');
        return equipamentos ? JSON.parse(equipamentos) : [];
    }

    carregarManutencoes() {
        const manutencoes = localStorage.getItem('qat_manutencoes');
        return manutencoes ? JSON.parse(manutencoes) : [];
    }

    salvarEquipamentos() {
        localStorage.setItem('qat_equipamentos', JSON.stringify(this.equipamentos));
    }

    salvarManutencoes() {
        localStorage.setItem('qat_manutencoes', JSON.stringify(this.manutencoes));
    }

    adicionarEquipamento(e) {
        e.preventDefault();
        
        const equipamento = {
            id: Date.now(),
            nome: document.getElementById('equipment-name').value,
            tipo: document.getElementById('equipment-type').value,
            localizacao: document.getElementById('equipment-location').value,
            status: document.getElementById('equipment-status').value,
            dataAquisicao: document.getElementById('equipment-date').value,
            dataCadastro: new Date().toISOString().split('T')[0]
        };

        this.equipamentos.push(equipamento);
        this.salvarEquipamentos();
        this.renderizarTabela();
        this.atualizarListaEquipamentos();
        this.limparFormulario('equipment-form');
        
        this.showNotification('Equipamento cadastrado com sucesso!', 'success');
    }

    editarEquipamento(id) {
        const equipamento = this.equipamentos.find(eq => eq.id === id);
        if (equipamento) {
            document.getElementById('equipment-name').value = equipamento.nome;
            document.getElementById('equipment-type').value = equipamento.tipo;
            document.getElementById('equipment-location').value = equipamento.localizacao;
            document.getElementById('equipment-status').value = equipamento.status;
            document.getElementById('equipment-date').value = equipamento.dataAquisicao;
            
            // Remover o equipamento atual para permitir atualização
            this.removerEquipamento(id, false);
        }
    }

    removerEquipamento(id, confirmar = true) {
        if (confirmar && !confirm('Tem certeza que deseja remover este equipamento?')) {
            return;
        }
        
        this.equipamentos = this.equipamentos.filter(eq => eq.id !== id);
        this.salvarEquipamentos();
        this.renderizarTabela();
        this.atualizarListaEquipamentos();
        
        if (confirmar) {
            this.showNotification('Equipamento removido com sucesso!', 'success');
        }
    }

    renderizarTabela() {
        const tbody = document.getElementById('equipments-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';
        
        this.equipamentos.forEach(equipamento => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${equipamento.nome}</td>
                <td>${equipamento.tipo}</td>
                <td>${equipamento.localizacao}</td>
                <td><span class="status-badge status-${equipamento.status}">${this.getStatusText(equipamento.status)}</span></td>
                <td>${this.formatDate(equipamento.dataAquisicao)}</td>
                <td>
                    <button onclick="equipamentosManager.editarEquipamento(${equipamento.id})" class="btn btn-sm btn-primary" title="Editar">
                        ✏️
                    </button>
                    <button onclick="equipamentosManager.removerEquipamento(${equipamento.id})" class="btn btn-sm btn-danger" title="Remover">
                        🗑️
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    filtrarEquipamentos(termo) {
        const linhas = document.querySelectorAll('#equipments-tbody tr');
        linhas.forEach(linha => {
            const texto = linha.textContent.toLowerCase();
            linha.style.display = texto.includes(termo.toLowerCase()) ? '' : 'none';
        });
    }

    limparFormulario(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    getStatusText(status) {
        const statusMap = {
            'ativo': 'Ativo',
            'manutencao': 'Em Manutenção',
            'inativo': 'Inativo'
        };
        return statusMap[status] || status;
    }

    formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR');
    }

    adicionarManutencao(e) {
        e.preventDefault();
        
        const manutencao = {
            id: Date.now(),
            equipamentoId: document.getElementById('maintenance-equipment').value,
            tipo: document.getElementById('maintenance-type').value,
            descricao: document.getElementById('maintenance-description').value,
            data: document.getElementById('maintenance-date').value,
            custo: parseFloat(document.getElementById('maintenance-cost').value) || 0,
            dataCadastro: new Date().toISOString().split('T')[0]
        };

        this.manutencoes.push(manutencao);
        this.salvarManutencoes();
        this.limparFormulario('maintenance-form');
        
        this.showNotification('Manutenção registrada com sucesso!', 'success');
    }

    atualizarListaEquipamentos() {
        const select = document.getElementById('maintenance-equipment');
        if (!select) return;

        // Limpar opções existentes (exceto a primeira)
        select.innerHTML = '<option value="">Selecione um equipamento...</option>';
        
        // Adicionar equipamentos ativos
        this.equipamentos
            .filter(eq => eq.status === 'ativo' || eq.status === 'manutencao')
            .forEach(equipamento => {
                const option = document.createElement('option');
                option.value = equipamento.id;
                option.textContent = `${equipamento.nome} - ${equipamento.tipo}`;
                select.appendChild(option);
            });
    }

    filtrarPorStatus(status) {
        const linhas = document.querySelectorAll('#equipments-tbody tr');
        linhas.forEach(linha => {
            if (!status) {
                linha.style.display = '';
            } else {
                const statusCell = linha.querySelector('.status-badge');
                const statusValue = statusCell ? statusCell.className.split('status-')[1] : '';
                linha.style.display = statusValue === status ? '' : 'none';
            }
        });
    }
}

// Funções globais para exportação e gráficos
function exportToPDF() {
    if (typeof jsPDF === 'undefined') {
        equipamentosManager.showNotification('Biblioteca jsPDF não carregada!', 'error');
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Título
    doc.setFontSize(20);
    doc.text('Relatório de Equipamentos', 20, 20);
    
    // Data
    doc.setFontSize(12);
    doc.text(`Gerado em: ${new Date().toLocaleDateString('pt-BR')}`, 20, 30);
    
    // Dados
    let yPosition = 50;
    equipamentosManager.equipamentos.forEach((equipamento, index) => {
        if (yPosition > 270) {
            doc.addPage();
            yPosition = 20;
        }
        
        doc.text(`${index + 1}. ${equipamento.nome} - ${equipamento.tipo} - ${equipamento.status}`, 20, yPosition);
        yPosition += 10;
    });
    
    doc.save('equipamentos.pdf');
    equipamentosManager.showNotification('PDF exportado com sucesso!', 'success');
}

function exportToCSV() {
    const data = equipamentosManager.equipamentos;
    if (!data.length) {
        equipamentosManager.showNotification('Nenhum equipamento para exportar!', 'warning');
        return;
    }
    
    const headers = ['Nome', 'Tipo', 'Localização', 'Status', 'Data Aquisição'];
    const csvContent = [
        headers.join(','),
        ...data.map(eq => [
            `"${eq.nome}"`,
            `"${eq.tipo}"`,
            `"${eq.localizacao}"`,
            `"${eq.status}"`,
            `"${eq.dataAquisicao}"`
        ].join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'equipamentos.csv';
    link.click();
    
    equipamentosManager.showNotification('CSV exportado com sucesso!', 'success');
}

function showBarChart() {
    const modal = document.getElementById('chart-modal');
    const canvas = document.getElementById('chart-canvas');
    
    if (!modal || !canvas) return;
    
    modal.style.display = 'block';
    
    // Dados para o gráfico
    const statusCount = equipamentosManager.equipamentos.reduce((acc, eq) => {
        acc[eq.status] = (acc[eq.status] || 0) + 1;
        return acc;
    }, {});
    
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: Object.keys(statusCount),
            datasets: [{
                label: 'Quantidade de Equipamentos',
                data: Object.values(statusCount),
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Equipamentos por Status'
                }
            }
        }
    });
}

function showPieChart() {
    const modal = document.getElementById('chart-modal');
    const canvas = document.getElementById('chart-canvas');
    
    if (!modal || !canvas) return;
    
    modal.style.display = 'block';
    
    // Dados para o gráfico
    const tipoCount = equipamentosManager.equipamentos.reduce((acc, eq) => {
        acc[eq.tipo] = (acc[eq.tipo] || 0) + 1;
        return acc;
    }, {});
    
    new Chart(canvas, {
        type: 'pie',
        data: {
            labels: Object.keys(tipoCount),
            datasets: [{
                data: Object.values(tipoCount),
                backgroundColor: [
                    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', 
                    '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribuição por Tipo de Equipamento'
                }
            }
        }
    });
}

function showLineChart() {
    equipamentosManager.showNotification('Gráfico de linha em desenvolvimento!', 'info');
}

function openPowerBI() {
    window.open('https://powerbi.microsoft.com/', '_blank');
}

function closeModal() {
    const modal = document.getElementById('chart-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function goBack() {
    window.history.back();
}

// Inicializar quando a página carregar
let equipamentosManager;
document.addEventListener('DOMContentLoaded', () => {
    equipamentosManager = new EquipamentosManager();
});