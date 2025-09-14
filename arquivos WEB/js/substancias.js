// Gerenciamento de Substâncias
class SubstanciasManager {
    constructor() {
        this.substancias = this.carregarSubstancias();
        this.initEventListeners();
        this.renderizarTabela();
    }

    initEventListeners() {
        const form = document.getElementById('substancia-form');
        if (form) {
            form.addEventListener('submit', (e) => this.adicionarSubstancia(e));
        }

        const searchInput = document.getElementById('search-substancias');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.filtrarSubstancias(e.target.value));
        }
    }

    carregarSubstancias() {
        const substancias = localStorage.getItem('qat_substancias');
        return substancias ? JSON.parse(substancias) : [];
    }

    salvarSubstancias() {
        localStorage.setItem('qat_substancias', JSON.stringify(this.substancias));
    }

    adicionarSubstancia(e) {
        e.preventDefault();
        
        const substancia = {
            id: Date.now(),
            nome: document.getElementById('nome').value,
            formula: document.getElementById('formula').value,
            massaMolar: parseFloat(document.getElementById('massa-molar').value),
            densidade: parseFloat(document.getElementById('densidade').value) || null,
            pontoFusao: parseFloat(document.getElementById('ponto-fusao').value) || null,
            pontoEbulicao: parseFloat(document.getElementById('ponto-ebulicao').value) || null,
            descricao: document.getElementById('descricao').value,
            dataCadastro: new Date().toISOString().split('T')[0]
        };

        this.substancias.push(substancia);
        this.salvarSubstancias();
        this.renderizarTabela();
        this.limparFormulario();
        
        this.showNotification('Substância cadastrada com sucesso!', 'success');
    }

    editarSubstancia(id) {
        const substancia = this.substancias.find(sub => sub.id === id);
        if (substancia) {
            document.getElementById('nome').value = substancia.nome;
            document.getElementById('formula').value = substancia.formula;
            document.getElementById('massa-molar').value = substancia.massaMolar;
            document.getElementById('densidade').value = substancia.densidade || '';
            document.getElementById('ponto-fusao').value = substancia.pontoFusao || '';
            document.getElementById('ponto-ebulicao').value = substancia.pontoEbulicao || '';
            document.getElementById('descricao').value = substancia.descricao;
            
            this.removerSubstancia(id, false);
        }
    }

    removerSubstancia(id, confirmar = true) {
        if (confirmar && !confirm('Tem certeza que deseja remover esta substância?')) {
            return;
        }
        
        this.substancias = this.substancias.filter(sub => sub.id !== id);
        this.salvarSubstancias();
        this.renderizarTabela();
        
        if (confirmar) {
            this.showNotification('Substância removida com sucesso!', 'success');
        }
    }

    renderizarTabela() {
        const tbody = document.querySelector('#substancias-table tbody');
        if (!tbody) return;

        tbody.innerHTML = '';
        
        this.substancias.forEach(substancia => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${substancia.nome}</td>
                <td>${substancia.formula}</td>
                <td>${substancia.massaMolar.toFixed(2)}</td>
                <td>${substancia.densidade ? substancia.densidade.toFixed(2) : '-'}</td>
                <td>${substancia.pontoFusao ? substancia.pontoFusao.toFixed(1) + '°C' : '-'}</td>
                <td>${substancia.pontoEbulicao ? substancia.pontoEbulicao.toFixed(1) + '°C' : '-'}</td>
                <td>
                    <button onclick="substanciasManager.editarSubstancia(${substancia.id})" class="btn btn-sm btn-primary" title="Editar">
                        ✏️
                    </button>
                    <button onclick="substanciasManager.removerSubstancia(${substancia.id})" class="btn btn-sm btn-danger" title="Remover">
                        🗑️
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    filtrarSubstancias(termo) {
        const linhas = document.querySelectorAll('#substancias-table tbody tr');
        linhas.forEach(linha => {
            const texto = linha.textContent.toLowerCase();
            linha.style.display = texto.includes(termo.toLowerCase()) ? '' : 'none';
        });
    }

    limparFormulario() {
        const form = document.getElementById('substancia-form');
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
}

// Função global para exportação
function exportSubstanciasPDF() {
    if (typeof jsPDF === 'undefined') {
        substanciasManager.showNotification('Biblioteca jsPDF não carregada!', 'error');
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Título
    doc.setFontSize(20);
    doc.text('Relatório de Substâncias', 20, 20);
    
    // Data
    doc.setFontSize(12);
    doc.text(`Gerado em: ${new Date().toLocaleDateString('pt-BR')}`, 20, 30);
    
    // Dados
    let yPosition = 50;
    substanciasManager.substancias.forEach((substancia, index) => {
        if (yPosition > 270) {
            doc.addPage();
            yPosition = 20;
        }
        
        doc.text(`${index + 1}. ${substancia.nome} (${substancia.formula}) - MM: ${substancia.massaMolar}g/mol`, 20, yPosition);
        yPosition += 10;
    });
    
    doc.save('substancias.pdf');
    substanciasManager.showNotification('PDF exportado com sucesso!', 'success');
}

// Inicializar quando a página carregar
let substanciasManager;
document.addEventListener('DOMContentLoaded', () => {
    substanciasManager = new SubstanciasManager();
});